import signal
import sys
import static
import os
import readline

def signal_handler(sig, frame):
        print(static.CTRL_C_TEXT)
        sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = options

    def complete(self, text, state):
        
        line = ' '.join(readline.get_line_buffer().split())

        if not line:
            return [c for c in self.options][state]
        else:
            return [c for c in self.options if line in c][state]

        try: 
            return self.matches[state]
        except IndexError:
            return None

def completer_update(item_list):
    completer = MyCompleter(item_list)
    readline.set_completer(completer.complete)
    readline.set_completer_delims('\t')
    readline.parse_and_bind('tab: complete')