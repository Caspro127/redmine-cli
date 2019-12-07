from redminelib import Redmine
import variables as var
from datetime import datetime
import readline


class RedmineManager():

    PROJECT_NAME = var.DEFAULT_PROJECT_NAME
    TRACKER_ID = var.DEFAULT_TRACKER_ID 
    USER_ID = var.DEFAULT_USER_ID

    def __init__(self):
        self.redmine = Redmine(var.REDMINE_URL, key=var.REDMINE_KEY)
        self.get_project_issues()
        self.get_project_users_list()
        self.get_my_issues()
        self.get_all_statuses()

    def get_project_issues(self, project_name = var.DEFAULT_PROJECT_NAME):
        self.project = self.redmine.project.get(project_name)
        self.issues_list = []
        #self.issues_id_list = []
        for issue in self.project.issues:
            df = {}
            df['id'] = issue.id
            df['subject'] = issue.subject
            df['status'] = issue.status['name']
            try:
                df['assigned_to'] = issue.assigned_to['name']
            except:
                df['assigned_to'] = 'Nobody'
            df['author'] = issue.author['name']
            df['priority'] = issue.priority['name']
            #self.issues_id_list.append(str(df['id']))
            self.issues_list.append(df)

    def get_all_statuses(self):

        self.status_dict = {}
        
        [self.status_dict.update({d.id : d.name}) for d in self.redmine.issue_status.all()]

        return self.status_dict

    def print_all_issues(self):
        print('-'*96)
        for issue in self.issues_list:
            fill = 0

            subject = issue['subject'][:40].split()
            subject = ' '.join(subject)
            if len(subject) < 40:
                fill = 40 - len(subject)
            subject = subject + ' ' * fill

            fill = 21 - len(str(issue['status']))
            status = str(issue['status'])[:21] + ' ' * fill
            try:
                fill = 19 - len(str(issue['assigned_to']))
            except:
                fill = 19
            to_do = ''
            try:
                if str(issue['assigned_to']) in var.IT_USER_LIST:
                    to_do = '<-- TO DO'
            except:
                pass
            try:
                assigned = str(issue['assigned_to']) + ' '* fill
            except:
                assigned = '' + ' '* fill
            print(f"#{issue['id']} - {subject} | {status} | {assigned} | {to_do}")
        print('-'*96)

    def get_user_activity(self, from_date=datetime.now().strftime('%Y-%m-%d'), to_date=datetime.now().strftime('%Y-%m-%d'), user_id=var.DEFAULT_USER_ID):
        
        self.activity_list = []

        times = self.redmine.time_entry.filter(user_id=user_id, from_date=from_date, to_date=to_date)

        [self.activity_list.append({
            'id':f.issue.id,
            'subject':self.redmine.issue.get(f.issue.id).subject,
            'time':f.hours, 
            'comments':f.comments
        }) for f in times]

        return self.activity_list

    def print_activity(self):

        title_subject = 'Subject'
        title_hours = 'Hours'
        title_comments = 'Comments'

        fills_subject = int((50 - len(title_subject))/2)
        title_subject = fills_subject * ' ' + title_subject + fills_subject * ' '

        fills_hours = int((10 - len(title_hours))/2)
        title_hours = fills_hours * ' ' + title_hours + fills_hours * ' '

        fills_comments = int((42 - len(title_comments))/2)
        title_comments = fills_comments * ' ' + title_comments + fills_comments * ' '

        title_footer = 'Total'
        fills = int((50 - len(title_footer))/2)

        footer = fills * ' ' + title_footer + fills * ' '
        footer = f"{footer}"

        print(f" {title_subject}{title_hours}{title_comments}")
        print('-'*100)
        for time in self.activity_list:
            fill = 0
            
            subject = time['subject'][:40].split()
            subject = ' '.join(subject)
            if len(subject) < 40:
                fill = 40 - len(subject)
            subject = subject + ' ' * fill
            
            fill = 6 - len(str(time['time'])+'h')
            hours = str(time['time']) + 'h' + ' ' * fill
            
            fill = 0
            comments = time['comments'][:40].split()
            comments = ' '.join(comments)
            if len(comments) < 40:
                fill = 40 - len(comments)
            comments = comments + ' ' * fill
            
            print(f"#{time['id']} - {subject} | {hours} | {comments}|")
                
        print('-'*100)
        sum_len = 6 - len(f"{sum([d['time'] for d in self.activity_list])}h")
        print(f" {footer}| {sum([d['time'] for d in self.activity_list])}h{sum_len * ' '} | ")

    def print_my_issues(self):
        print('-'*96)
        for issue in self.my_issues_list:
            fill = 0

            subject = issue['subject'][:40].split()
            subject = ' '.join(subject)
            if len(subject) < 40:
                fill = 40 - len(subject)
            subject = subject + ' ' * fill

            fill = 21 - len(str(issue['status']))
            status = str(issue['status'])[:21] + ' ' * fill
            try:
                fill = 19 - len(str(issue['assigned_to']))
            except:
                fill = 19
            try:
                assigned = str(issue['assigned_to']) + ' '* fill
            except:
                assigned = '' + ' ' * fill
            print(f"#{issue['id']} - {subject} | {status} | {assigned} | ")
        print('-'*96)
    
    def add_time_entry(self, id, amount_time, description, assign_to_id, status_id, done_ratio, date=datetime.now().strftime('%Y-%m-%d')):
        response = []
        try:
            tmp_resp = self.redmine.time_entry.create(
                issue_id=id,
                spent_on=date,
                hours=amount_time,
                comments=description
            )
            response.append(tmp_resp)
        except Exception as e:
            print(f"Except 1 - {e}")

        try:
            tmp_resp = self.redmine.issue.update(
                resource_id = id,
                assigned_to_id = assign_to_id,
                status_id = status_id,
                notes = description,
                done_ratio = done_ratio
            )
            response.append(tmp_resp)
        except Exception as e:
            print(f"Except 2 - {e}")
        
        return response

    def print_description_and_comments(self, id):
        issue = self.redmine.issue.get(id, include=['journals'])
        print()
        print(f"#{issue.id}-{issue.subject}")
        print()
        print(f"Author: {issue.author}")
        print()
        print("#"*40)
        print("Description:")
        print("#"*40)
        print()
        print(issue.description)

        print()
        print("#"*40)
        print("Comments:")
        print("#"*40)
        print()

        if len(issue.journals) > 3:
            journals = issue.journals[-3:]
        else:
            journals = issue.journals
            
        for journal in journals:
            print(f"{journal.created_on} - {journal.user}:")
            print(f"{journal.notes}")
            print()


    def get_project_users_list(self):
        self.project_users = []
        self.users_name_list = []
        for user in self.project.memberships:
            df = {}
            try:
                df['id'] = user.user.id
                df['name'] = user.user.name
                if int(user.user.id) == int(self.USER_ID):
                    self.USER_NAME = user.user.name
                self.users_name_list.append(df['name'])
                self.project_users.append(df)
            except Exception as e:
                pass
        return self.project_users

    def get_my_issues(self, user_name=''):

        if user_name == '':
            user_name = self.USER_NAME
        else:
            self.DEFAULT_USER_NAME = self.USER_NAME
            self.USER_NAME = user_name

        self.my_issues_list = []
        for issue in self.issues_list:
            if user_name == issue['assigned_to']:
                self.my_issues_list.append(issue)
        return self.my_issues_list

    def create_task(self, subject, description, due_date, assigned_to_id=4):
        if assigned_to_id != 4:
            try:
                issue = self.redmine.issue.create(
                    project_id=self.project.id,
                    subject=subject,
                    tracker_id=self.TRACKER_ID,
                    description=description,
                    assigned_to_id=assigned_to_id,
                    due_date=due_date
                )
            except Exception as e:
                print(f"Niepowodzenie zakładania zadania - {e}")
                exit(5)
        else:
            try:
                issue = self.redmine.issue.create(
                    project_id=self.project.id,
                    subject=subject,
                    tracker_id=self.TRACKER_ID,
                    description=description,
                    due_date=due_date
                )
            except Exception as e:
                print(f"Niepowodzenie zakładania zadania - {e}")
                exit(5)        
        print("\nUtworzono zadanie nr: " + str(issue.id) + " o nazwie "+ '"' + str(issue.subject)+'"')
        return {'id':issue.id, 'subject':issue.subject}

    def update_task(self, id, assign_to_id, status_id, done_ratio):
        try:
            response = self.redmine.issue.update(
                resource_id = id,
                assigned_to_id = assign_to_id,
                status_id = status_id,
                done_ratio = done_ratio
            )
        except Exception as e:
            print(f"Except 2 - {e}")
        return response

    def assign_task(self, id, assign_to):
        try:
            self.redmine.issue.update(
                resource_id=id,
                assigned_to_id = assign_to
            )
        except Exception as e:
            print(f"Except 2 - {e}")
