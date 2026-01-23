from pywhispercpp.model import Model

# Initialize the model
model = Model('small.en' , n_threads=4)  # Options: tiny, base, small, medium, large


def transcribe(filename):
    # Transcribe audio
    segments = model.transcribe(filename)

    formatted_segments = []
    for segment in segments:
        formatted_segment =f"{segment.text}" #[{segment.t0:.2f}s -> {segment.t1:.2f}s]     [{segment.t0:.2f}s -> {segment.t1:.2f}s]
        formatted_segments.append(formatted_segment)
    return '\n'.join(formatted_segments)

if __name__ == '__main__':
    transcription = transcribe('Store.m4a')
    print(transcription)