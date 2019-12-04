import signal
import sys
import static
import os

def signal_handler(sig, frame):
        print(static.CTRL_C_TEXT)
        sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)