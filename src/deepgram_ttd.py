from deepgram import DeepgramClient
import subprocess
import os
import tempfile
from config import Deepgram_key


def transcribe(filename):
    """
    Transcribe audio file with aggressive preprocessing for scanner audio.
    """
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_wav.close()
    client = DeepgramClient(api_key=Deepgram_key)

    try:
        # audio enhancement
        print(f"Converting and enhancing {filename}...")

        # Multi-stage audio filtering:
        # 1. Remove very low/high frequencies
        # 2. Reduce background noise
        # 3. Normalize volume
        # 4. Compress dynamic range for consistent volume
        """filters = [
            'highpass=f=300',  # Remove low rumble
            'lowpass=f=3000',  # Remove high static
            'afftdn=nf=-25',  # Noise reduction
            'loudnorm=I=-16:TP=-1.5',  # Normalize loudness
            'compand=attacks=0.3:decays=0.8:points=-80/-80|-45/-15|-27/-9|0/-7|20/-7'  # Compress dynamics
        ]"""
        filters = [
            'highpass=f=80',
            'afftdn=nf=-30',
            'loudnorm=I=-16:TP=-1.5',
        ]

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                filename,
                "-af",
                ",".join(filters),
                "-ar",
                "16000",
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                "-y",
                temp_wav.name,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        if not os.path.exists(temp_wav.name) or os.path.getsize(temp_wav.name) == 0:
            raise Exception("FFmpeg created an empty output file")

        print(f"Transcribing...")

        with open(temp_wav.name, "rb") as audio:
            source = audio.read()

        print(temp_wav.name)
        print(os.path.getsize(temp_wav.name))


        # Transcribe the audio
        segments = client.listen.v1.media.transcribe_file(
            request=source,
            model="nova-3",
            language='en',
            smart_format=True,
            punctuate=True,
            utterances=True,
            numerals=True,
            keyterm=[
                'Cantril',
                'Milton',
                '10-22',
                'West Responders',
                'Van Buren county',
                'fire',
            ],
        )

        alt = segments.results.channels[0].alternatives[0]
        print(alt.transcript)

        result = alt.transcript

        # Debug output
        if not result.strip():
            print("Warning: No speech detected after filtering")
            return "[NO_SPEECH_DETECTED]"
        #print(f"Temp wav saved at: {temp_wav.name}")
        return result

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion error: {e.stderr}")
        raise Exception(f"Failed to convert audio file: {e.stderr}")
    except Exception as e:
        print(f"Transcription error: {e}")
        raise



    finally:
        if os.path.exists(temp_wav.name):
            os.unlink(temp_wav.name)



if __name__ == '__main__':
    #transcription = transcribe('Store.m4a') #Douds_fire_2026_02_06_16_30_14.wav
    transcription = transcribe('Douds_fire_2026_02_06_16_30_14.wav')  # Douds_fire_2026_02_06_16_30_14.wav
    print(f"Result: {transcription}")
else:
    print("Usage: python wisper.py <audio_file>")