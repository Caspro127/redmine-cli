#!/usr/bin/python3
import static
import events_handler
import readline
import time

print("Initializing....")
import menu_handler
from datetime import datetime, timedelta

clear = lambda: events_handler.os.system('clear')

def validate_menu_option():
    while True:
        try:
            choosen = input(static.PROMPT_TEXT)
            choosen = int(choosen)
            break
        except (ValueError):
            print("\n" + static.BAD_CHOOOSE_TEXT + "\n")
        except Exception as e:
            print(e)
            return 9
    return choosen

clear()
print(static.MAIN_TEXT)

while True:

    print(static.MAIN_MENU_TEXT)  
    choosen = validate_menu_option()

    if choosen == 0:
        menu_handler.print_all_tasks()

    elif choosen == 1:
        menu_handler.print_user_task()

    elif choosen == 2:
        menu_handler.add_time_to_task()
        print('Done!')
        time.sleep(0.5)
        clear()

    elif choosen == 3:
        menu_handler.get_user_activity()

    elif choosen == 4:
        menu_handler.create_new_task()
        print("Done!")
        time.sleep(0.5)
        clear()
            
    elif choosen == 5:
        menu_handler.list_somebody_tasks()

    elif choosen == 6:
        menu_handler.create_new_task_with_defaults()
        print("Done!")
        time.sleep(0.5)
        clear()

    elif choosen == 7:
        menu_handler.assign_task_to_somebody()
        time.sleep(0.5)
        print("Done!")
        clear()

    elif choosen == 8:
        menu_handler.show_desc_and_comment()
        input(static.ENTER_KEY_TEXT)
        clear()

    elif choosen == 9:
        print("Soo this is the end...")
        events_handler.sys.exit(0)
    