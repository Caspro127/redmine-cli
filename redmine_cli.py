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

    if choosen == 0:
        redmine.get_project_issues(redmine.PROJECT_NAME)
        redmine.print_all_issues()
        input(static.ENTER_KEY_TEXT)

    elif choosen == 1:
        redmine.get_project_issues(redmine.PROJECT_NAME)
        redmine.get_my_issues()
        redmine.print_my_issues()
        input(static.ENTER_KEY_TEXT)

    elif choosen == 2:
        completer_update([str(d['id']) for d in redmine.issues_list])
        print([d['id'] for d in redmine.issues_list])
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

        issue = redmine.redmine.issue.get(id)
        completer_update([f for d,f in redmine.get_all_statuses().items()])
        while True:
            try:
                status = input(f"Status ({issue.status.name}): ")
                if status == '':
                    status_id = issue.status.id
                    break
                else:
                    status_id = [d for d,f in redmine.get_all_statuses().items() if f == status][0]
                    break
            except (ValueError):
                print("Bad value, try again")
            except Exception as e:
                print(e)

        try:
            done_ratio = input(f"Done Ratio ({issue.done_ratio}): ")
            if done_ratio == '':
                done_ratio = issue.done_ratio
            else:
                try:
                    done_ratio = int(done_ratio)
                    if done_ratio > 100 or done_ratio < 0:
                        raise ValueError
                except (ValueError):
                    print("Bad value - passing...")
                    done_ratio = issue.done_ratio
        except Exception as e:
            print(e)
            done_ratio = issue.done_ratio

        completer_update(redmine.users_name_list)

        try:
            assign_to = input(f"Assign ({issue.assigned_to}): ")
            if assign_to == '':
                assign_to_id = issue.assigned_to.id
            else:
                assign_to_id = [d['id'] for d in redmine.project_users if d['name'] == assign_to][0]

        except (KeyError):
            assign_to = input(f"Assign: ")
            if assign_to == '':
                assign_to_id = issue.assigned_to.id
            else:
                assign_to_id = [d['id'] for d in redmine.project_users if d['name'] == assign_to][0]        
        except Exception as e:
            print(e)
            assign_to_id = 4

        while True:
            description = input("Description: ")
            if description == '':
                print("Description can't be blank ")
            else:
                break

        date = input(f"Date (default {datetime.now().strftime('%Y-%m-%d')})")
        if date == '':
            date = datetime.now().strftime('%Y-%m-%d')
        response = redmine.add_time_entry(id, amount_time, description, assign_to_id, status_id, done_ratio, date)
        print(response)
        input(static.ENTER_KEY_TEXT)
        clear()

    elif choosen == 3:
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

    elif choosen == 4:
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
            

        

    elif choosen == 5:
        print("List somebody else tasks")
        completer_update(redmine.users_name_list)
        name = input("Who's list? ")
        default_name = redmine.USER_NAME 
        redmine.get_my_issues(name)
        redmine.print_my_issues()
        redmine.get_my_issues(default_name)
        input(static.ENTER_KEY_TEXT)
        clear()


    elif choosen == 6:
        subject = input("Subject: ")
        description = input("Description: ")
        redmine.create_task(subject=subject, description=description, due_date=(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'), assigned_to_id=4)
        input(static.ENTER_KEY_TEXT)
        clear()

    elif choosen == 7:
        completer_update([str(d['id']) for d in redmine.issues_list])
        try:
            id = int(input("ID: "))
        except Exception as e:
            print(e)
            continue

        issue = redmine.redmine.issue.get(id)
        completer_update(redmine.users_name_list)
        try:
            assign_to = input(f"Assign ({issue.assigned_to}): ")
            if assign_to == '':
                assign_to_id = issue.assigned_to.id
            else:
                assign_to_id = [d['id'] for d in redmine.project_users if d['name'] == assign_to][0]

        except:
            try:
                assign_to = input(f"Assign: ")
                if assign_to == '':
                    assign_to_id = issue.assigned_to.id
                else:
                    assign_to_id = [d['id'] for d in redmine.project_users if d['name'] == assign_to][0]
            except Exception as e:
                print(e)
                assign_to_id = 4


        
        completer_update([f for d,f in redmine.get_all_statuses().items()])
        while True:
            try:
                status = input(f"Status ({issue.status.name}): ")
                if status == '':
                    status_id = issue.status.id
                    break
                else:
                    status_id = [d for d,f in redmine.get_all_statuses().items() if f == status][0]
                    break
            except (ValueError):
                print("Bad value, try again")
            except Exception as e:
                print(e)

        try:
            done_ratio = input(f"Done Ratio ({issue.done_ratio}): ")
            if done_ratio == '':
                done_ratio = issue.done_ratio
            else:
                try:
                    done_ratio = int(done_ratio)
                    if done_ratio > 100 or done_ratio < 0:
                        raise ValueError
                except (ValueError):
                    print("Bad value - passing...")
                    done_ratio = issue.done_ratio
        except Exception as e:
            print(e)
            done_ratio = issue.done_ratio

        except Exception as e:
            print(e)
            continue

        redmine.update_task(id, assign_to_id, status_id, done_ratio)
        print("Done!")
        input(static.ENTER_KEY_TEXT)
        clear()

    elif choosen == 9:
        print("Soo this is the end...")
        events_handler.sys.exit(0)
    