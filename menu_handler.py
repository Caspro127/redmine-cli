import redmine_handler
import readline
import variables as var
import redmine_handler
import events_handler
from datetime import datetime, timedelta

redmine = redmine_handler.RedmineManager()

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

def completer_update(item_list):
    completer = redmine_handler.MyCompleter(item_list)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

def print_all_tasks():
    redmine.get_project_issues(redmine.PROJECT_NAME)
    redmine.print_all_issues()

def print_user_task():
    redmine.get_project_issues(redmine.PROJECT_NAME)
    redmine.get_my_issues()
    redmine.print_my_issues()

def add_time_to_task():
    events_handler.completer_update([str(d['id']) for d in redmine.issues_list])
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
    events_handler.completer_update([f for d,f in redmine.get_all_statuses().items()])
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

    events_handler.completer_update(redmine.users_name_list)

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

def get_user_activity():
    date = validate_date(input(f"Date ({datetime.now().strftime('%Y-%m-%d')}): "))
    events_handler.completer_update(redmine.users_name_list)
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
        return
    
    redmine.get_user_activity(from_date=date, to_date=date, user_id=username)
    redmine.print_activity()

def create_new_task():
    subject = input("Subject: ")
    description = input("Description: ")
    events_handler.completer_update(redmine.users_name_list)
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
        return
    redmine.create_task(subject=subject, description=description, due_date=date, assigned_to_id=assigned_to)

def list_somebody_tasks():
    print("List somebody else tasks")
    events_handler.completer_update(redmine.users_name_list)
    name = input("Who's list? ")
    default_name = redmine.USER_NAME 
    redmine.get_my_issues(name)
    redmine.print_my_issues()
    redmine.get_my_issues(default_name)

def create_new_task_with_defaults():
    subject = input("Subject: ")
    description = input("Description: ")
    redmine.create_task(subject=subject, description=description, due_date=(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'), assigned_to_id=4)

def assign_task_to_somebody():
    events_handler.completer_update([str(d['id']) for d in redmine.issues_list])
    try:
        id = int(input("ID: "))
    except Exception as e:
        print(e)
        return
    issue = redmine.redmine.issue.get(id)
    events_handler.completer_update(redmine.users_name_list)
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
    events_handler.completer_update([f for d,f in redmine.get_all_statuses().items()])
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
        return
    redmine.update_task(id, assign_to_id, status_id, done_ratio)

def show_desc_and_comment():
    events_handler.completer_update([str(d['id']) for d in redmine.issues_list])
    try:
        id = int(input("ID: "))
    except Exception as e:
        print(e)
        return

    redmine.print_description_and_comments(id)










