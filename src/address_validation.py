import re
from urllib.parse import quote_plus

SUFFIXES = (
    "Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|"
    "Court|Ct|Way|Place|Pl|Highway|Hwy|Circle|Cir|Terrace|Ter|"
    "Trail|Trl|Parkway|Pkwy|Alley|Aly|Loop|Ridge|Point|Pt|Square|Sq|"
    "Pike|Path|Row|Crossing|Xing"
)
DIRS = (
    "Northeast|Northwest|Southeast|Southwest|North|South|East|West|"
    "NE|NW|SE|SW|N|S|E|W"
)

# Every town these calls come from is in Van Buren County, so the county
# is used in the link when no town is mentioned.
TOWNS = {'milton','cantril','douds','bonaparte','farmington','keosauqua','stockport','birmingham',}
COUNTY = "Van Buren County"

TOWN_PATTERN = "|".join(
    re.escape(t).replace(r"\ ", r"\s+")
    for t in sorted(TOWNS, key=len, reverse=True)
)
TOWN_RE = re.compile(rf"\b(?:{TOWN_PATTERN})\b", re.I)

# Small words that show up between a number and a street in dispatch
# speech ("Engine 2 respond to Main Street"). They're never allowed to be
# part of a street name, so they can't get pulled into the address.
STOPWORDS = (
    "to|of|at|in|on|the|a|an|and|or|for|by|near|from|with|is|are|"
    "respond|responding|reported|report|fire|block"
)
# A street name word: a regular word ("Jasper", "O'Brien") or an
# ordinal ("200th"), but never a bare number or a stopword.
WORD = rf"(?!(?:{STOPWORDS})\b)(?:[A-Za-z][A-Za-z'.]*|\d+(?:st|nd|rd|th))"
# Same, but must start with a capital letter. Used where there's no house
# number to anchor the match, so lowercase speech isn't mistaken for a street.
CAP_WORD = rf"(?!(?:{STOPWORDS})\b)(?:(?-i:[A-Z])[A-Za-z'.]*|\d+(?:st|nd|rd|th))"

# Numbered roads: "Highway 2", "Hwy 1", "US Highway 34", "Iowa 2",
# "County Road J40", "Route J 40".
ROUTE = (
    r"(?:(?:US|U\.S\.|Iowa|IA|State|County)\s+)?"
    r"(?:Highway|Hwy|Route|Rte|Road|Rd)\s+(?:[A-Z][\s-]?)?\d{1,3}[A-Z]?\b"
    r"|(?:US|U\.S\.|Iowa|IA)\s+\d{1,3}\b"
    r"|[A-Z]-?\d{2,3}\b"
)


def _street(word):
    return (
        rf"(?:(?:{DIRS})\.?\s+)?"
        rf"{word}(?:\s+{word}){{0,2}}?\s+"
        rf"(?:{SUFFIXES})\b\.?"
    )


ROAD = rf"(?:{ROUTE}|{_street(WORD)})(?:\s+(?:{DIRS})\b(?!\s+of\b))?"
CAP_ROAD = rf"(?:{ROUTE}|{_street(CAP_WORD)})"

ADDR_RE = re.compile(
    rf"(?<![\d:-])\b(?P<num>\d{{1,5}})\s+"
    rf"(?:block\s+of\s+)?"  # "the 500 block of Main Street"
    rf"(?P<road>{ROAD})"
    rf"(?:,?\s+(?:Apartment|Apt|Unit|Lot|Suite|Trailer)\s*#?\s*(?P<unit>\w+))?",
    re.I,
)

# "Main Street and Elm Street", "Highway 1 & 200th Street"
INTERSECTION_RE = re.compile(
    rf"\b(?P<a>{CAP_ROAD})\s+(?:and|&|at)\s+(?P<b>{CAP_ROAD})",
    re.I,
)


def _clean(s):
    return re.sub(r"[\s,]+", " ", s).strip()


def find_town(text, start, end):
    """Return the town mentioned closest to text[start:end], ignoring any
    that are part of the address itself (e.g. "Milton Street")."""
    best = None
    for m in TOWN_RE.finditer(text):
        if m.start() < end and m.end() > start:
            continue
        dist = m.start() - end if m.start() >= end else start - m.end()
        if best is None or dist < best[0]:
            best = (dist, m.group(0))
    return best[1].title() if best else None


def build_link(street, town, state="IA", unit=None):
    # Google Maps doesn't need the unit to find a building,
    # so it's left out of the query by default.
    q = f"{street}, {town or COUNTY}, {state}"
    return (
        "\nhttps://www.google.com/maps/search/?api=1"
        f"&query={quote_plus(q)}"
    )


def extract_address(text):
    m = ADDR_RE.search(text)
    if m:
        street = f"{m['num']} {_clean(m['road'])}"
        unit = m["unit"]
    else:
        m = INTERSECTION_RE.search(text)
        if not m:
            return ''
        street = f"{_clean(m['a'])} & {_clean(m['b'])}"
        unit = None
    return {"street": street, "town": find_town(text, m.start(), m.end()), "unit": unit}

def link_from_text(text, state="IA"):
    """Extract an address from text and return a Google Maps link,
    or '' if no address was found."""
    addr = extract_address(text)
    if not addr:
        return ''
    return build_link(addr["street"], addr["town"], state)

if __name__ == "__main__":
    transcription = ''
    print(extract_address(transcription))
    link = link_from_text(transcription)
    print(link)
