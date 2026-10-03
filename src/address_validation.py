import re
from urllib.parse import quote_plus

SUFFIXES = (
    "Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|"
    "Court|Ct|Way|Place|Pl|Highway|Hwy|Circle|Cir|Terrace|Ter"
)
DIRS = "North|South|East|West|N|S|E|W"

TOWNS = {'milton','cantril','douds','bonaparte','farmington','keosauqua','stockport','birmingham',}

TOWN_PATTERN = "|".join(
    re.escape(t).replace(r"\ ", r"\s+")
    for t in sorted(TOWNS, key=len, reverse=True)
)

ADDR_RE = re.compile(
    rf"\b(?P<num>\d{{1,5}})\s+"
    rf"(?P<dir>(?:{DIRS})\.?\s+)?"
    rf"(?P<name>[A-Za-z0-9]+(?:\s[A-Za-z0-9]+){{0,2}}?)\s+"
    rf"(?P<suffix>{SUFFIXES})\b\.?"
    rf"(?:,?\s+(?P<town>{TOWN_PATTERN})\b)?"
    rf"(?:,?\s+(?:Apartment|Apt|Unit|Lot|Suite)\s+(?P<unit>\w+))?",
    re.I,
)


def build_link(street, town, state="IA", unit=None):
    # Google Maps doesn't need the unit to find a building,
    # so it's left out of the query by default.
    q = f"{street}, {town}, {state}"
    return (
        "\nhttps://www.google.com/maps/search/?api=1"
        f"&query={quote_plus(q)}"
    )


def extract_address(text):
    m = ADDR_RE.search(text)
    if not m:
        return ''
    street = " ".join(
        p.strip() for p in (m["num"], m["dir"] or "", m["name"], m["suffix"]) if p.strip()
    )
    return {"street": street, "town": m["town"], "unit": m["unit"]}

def link_from_text(text, state="IA"):
    """Extract an address from text and return a Google Maps link,
    or None if no address was found."""
    addr = extract_address(text)
    if not addr:
        return ''
    return build_link(addr["street"], addr["town"], state)

if __name__ == "__main__":
    transcription = ''
    print(extract_address(transcription))
    link = link_from_text(transcription)
    print(link)