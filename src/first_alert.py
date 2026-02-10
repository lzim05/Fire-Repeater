#!/usr/bin/env python3
import sys
import asyncio
from telegram_bot import alert

def main():
	tone = sys.argv[1]
	time = sys.argv[2]
	message = f"{tone}'\nFirst Alert\n'{time}"
	print(message)
	
	asyncio.run(alert(message))
if __name__ == "__main__":
	main()