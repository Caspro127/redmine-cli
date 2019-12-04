import redmine_handler
import readline

def completer_update(item_list):
    completer = redmine_handler.MyCompleter(item_list)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

def all_tasks_menu():
    pass