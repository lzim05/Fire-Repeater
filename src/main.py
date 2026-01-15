#!/usr/bin/env python3
import sys
import os
from pathlib import Path


def main():
    # Get audio file path from command line
    audio_file = sys.argv[1]

    # 1. Upload to GCS (for backup/archive)
    gcs_url = upload_to_gcs(audio_file)

    # 2. Send SMS alert (fast, fire and forget)
    send_sms_alert()

    # 3. Upload audio to Telegram
    telegram_message = upload_to_telegram(audio_file)

    # 4. Transcribe with Whisper
    transcription = transcribe_audio(audio_file)

    # 5. Send transcription to Telegram
    send_transcription_to_telegram(transcription)


if __name__ == "__main__":
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
