#!/usr/bin/env python3
import sys
import asyncio
import traceback
import datetime
import os
from wisper import transcribe
from telegram_bot import group_message, audio_message


def main():
    tone = sys.argv[1]
    audio = sys.argv[2]
    asyncio.run(audio_message(audio))
    transcription = transcribe(audio)
    print(transcription)
    asyncio.run(group_message(transcription))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(script_dir, "error_log.txt")

        # Print to console
        print(f"\n=== ERROR DETAILS ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        print(f"===================\n")

        # Try to write to log file
        try:
            with open(log_path, "a") as log_file:
                current_time = datetime.datetime.now()
                time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"\n{'=' * 50}\n")
                log_file.write(f"--- Error Occurred ---\n")
                log_file.write(f"Time: {time_string}\n")
                log_file.write(f"Error type: {type(e).__name__}\n")
                log_file.write(f"Error message: {str(e)}\n")
                log_file.write(f"\nFull traceback:\n")
                traceback.print_exc(file=log_file)
                log_file.write(f"\n{'=' * 50}\n")

            print(f"Error logged to: {log_path}")
        except Exception as log_error:
            print(f"FAILED to write to log file: {log_error}")
            print(f"Attempted log path: {log_path}")

        sys.exit(1)