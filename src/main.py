#!/usr/bin/env python3
import asyncio
from wisper import transcribe
from telegram_bot import group_message


def main():
    try:
        transcription = transcribe('Store.m4a')
        print(transcription)
        asyncio.run(group_message('Store.m4a',transcription))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
