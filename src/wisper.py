from pywhispercpp.model import Model

# Initialize the model
model = Model('small.en' , n_threads=4)  # Options: tiny, base, small, medium, large


def transcribe(filename):
    # Transcribe audio
    segments = model.transcribe(filename)

    # Print results
    #for segment in segments:
        #return(f"[{segment.t0:.2f}s -> {segment.t1:.2f}s]{segment.text}") #[{segment.t0:.2f}s -> {segment.t1:.2f}s]
    return segments

if __name__ == '__main__':
    transcription = transcribe('Store.m4a')
    for segment in transcription:
        print(segment)