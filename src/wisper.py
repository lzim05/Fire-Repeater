from pywhispercpp.model import Model
import subprocess
import os
import tempfile

model = Model('base.en', n_threads=4)


def transcribe(filename):
    """
    Transcribe audio file with aggressive preprocessing for scanner audio.
    """
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_wav.close()

    try:
        # audio enhancement
        print(f"Converting and enhancing {filename}...")

        # Multi-stage audio filtering:
        # 1. Remove very low/high frequencies
        # 2. Reduce background noise
        # 3. Normalize volume
        # 4. Compress dynamic range for consistent volume
        filters = [
            'highpass=f=300',  # Remove low rumble
            'lowpass=f=3000',  # Remove high static
            'afftdn=nf=-25',  # Noise reduction
            'loudnorm=I=-16:TP=-1.5',  # Normalize loudness
            'compand=attacks=0.3:decays=0.8:points=-80/-80|-45/-15|-27/-9|0/-7|20/-7'  # Compress dynamics
        ]

        result = subprocess.run([
            'ffmpeg', '-i', filename,
            '-ar', '16000',
            '-ac', '1',
            '-af', ','.join(filters),
            '-ss', '3',
            '-y',
            temp_wav.name
        ], check=True, capture_output=True, text=True)

        print(f"Transcribing...")

        # Transcribe the audio
        segments = model.transcribe(temp_wav.name)

        formatted_segments = []
        for segment in segments:
            text = segment.text.strip()
            # Filter out non-speech markers
            if text and text not in ['[BLANK_AUDIO]', '[SOUND]', '[MUSIC]']:
                formatted_segments.append(text)

        result = ' '.join(formatted_segments)

        # Debug output
        if not result.strip():
            print("Warning: No speech detected after filtering")
            return "[NO_SPEECH_DETECTED]"

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
    transcription = transcribe('Douds_fire_2026_02_06_16_30_14.wav')
    print(f"Result: {transcription}")
else:
    print("Usage: python wisper.py <audio_file>")