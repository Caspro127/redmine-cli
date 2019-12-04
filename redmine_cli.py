#!/usr/bin/python3
import redmine_handler
import static
import events_handler
import readline
import menu_handler
from datetime import datetime, timedelta

print("Initializing....")
redmine = redmine_handler.RedmineManager()
clear = lambda: events_handler.os.system('clear')

def completer_update(item_list):
    completer = redmine_handler.MyCompleter(item_list)
    readline.set_completer(completer.complete)
    readline.set_completer_delims('\t')
    readline.parse_and_bind('tab: complete')

def validate_date(date):
    try:
        if date == '':
            return datetime.now().strftime('%Y-%m-%d')
        else:
            datetime.strptime(date,"%Y-%m-%d")
            return date
    except (ValueError):
        print("Bad value, set today")
        return datetime.now().strftime('%Y-%m-%d')
    except Exception as e:
        print(e)

clear()
print(static.MAIN_TEXT)

while True:

    print(static.MAIN_MENU_TEXT)  
    while True:
        try:
            choosen = input(static.PROMPT_TEXT)
            choosen = int(choosen)
            break
        except (ValueError):
            print("\n" + static.BAD_CHOOOSE_TEXT + "\n")
        except Exception as e:
            print(e)
            choosen = 9

    if choosen == 1:
        redmine.get_project_issues(redmine.PROJECT_NAME)
        redmine.print_all_issues()
        input(static.ENTER_KEY_TEXT)

    elif choosen == 2:
        redmine.print_my_issues()
        input(static.ENTER_KEY_TEXT)

    elif choosen == 3:
        completer_update(redmine.issues_id_list)
        while True:
            try:
                id = int(input("Task ID: "))
                break
            except (ValueError):
                print("Bad value, try again")
            except Exception as e:
                print(e)

        while True:
            try:
                amount_time = float(input("Time: "))
                break
            except (ValueError):
                print("Bad value, try again")
            except Exception as e:
                print(e)

        description = input("Description: ")
        date = input(f"Date (default {datetime.now().strftime('%Y-%m-%d')})")
        if date == '':
            date = datetime.now().strftime('%Y-%m-%d')
        response = redmine.add_time_entry(id, amount_time, description, date)
        print(response)
        input(static.ENTER_KEY_TEXT)
        clear()

    elif choosen == 4:
        date = validate_date(input(f"Date ({datetime.now().strftime('%Y-%m-%d')}): "))
        completer_update(redmine.users_name_list)
        username = input(f"User Name ({redmine.USER_NAME}): ")
        if username == '':
            username = redmine.USER_NAME
        try:
            username = [d['id'] for d in redmine.project_users if d['name'] == username]
            if username == []:
                username == redmine.USER_ID
            else:
                username == int(username[0])
        except Exception as e:
            print(e)
            continue
        
        redmine.get_user_activity(from_date=date, to_date=date, user_id=username)
        redmine.print_activity()
        input(static.ENTER_KEY_TEXT)

    elif choosen == 5:
        subject = input("Subject: ")
        description = input("Description: ")
        completer_update(redmine.users_name_list)
        assigned_to = input("Assign to: ")
        date = input(f"Due Date ({(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}): ")
        if date == '':
            date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        try:
            assigned_to = [d['id'] for d in redmine.project_users if d['name'] == assigned_to]
            if assigned_to == []:
                assigned_to == 4
            else:
                assigned_to == int(assigned_to[0])
        except Exception as e:
            print(e)
            continue
        redmine.create_task(subject=subject, description=description, due_date=date, assigned_to_id=assigned_to)
        input(static.ENTER_KEY_TEXT)
        clear()
            

        

    elif choosen == 6:
        print("List somebody else tasks")
        completer_update(redmine.users_name_list)
        name = input("Who's list? ")
        default_name = redmine.USER_NAME 
        redmine.get_my_issues(name)
        redmine.print_my_issues()
        redmine.get_my_issues(default_name)
        input(static.ENTER_KEY_TEXT)
        clear()


    elif choosen == 7:
        subject = input("Subject: ")
        description = input("Description: ")
        redmine.create_task(subject=subject, description=description, due_date=(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'), assigned_to_id=4)
        input(static.ENTER_KEY_TEXT)
        clear()

    elif choosen == 8:
        completer_update(redmine.issues_id_list)
        try:
            task_id = int(input("ID: "))
        except Exception as e:
            print(e)
            continue
        completer_update(redmine.users_name_list)
        try:
            assign_to = input("Assign To: ").split()
            assign_to = ' '.join(assign_to)
            assign_to = [d['id'] for d in redmine.project_users if d['name'] == assign_to][0]
        except Exception as e:
            print(e)
            continue


        redmine.assign_task(task_id, assign_to)
        input(static.ENTER_KEY_TEXT)
        clear()


    elif choosen == 9:
        print("Soo this is the end...")
        events_handler.sys.exit(0)
    