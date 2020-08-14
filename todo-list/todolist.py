import sys
from datetime import datetime
from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.now())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class ToDo:
    def __init__(self, session):
        self.session = session
        self.menu_options = {
            1: {'display_text': "Today's tasks", 'handler': self.todays_tasks},
            2: {'display_text': "Week's tasks", 'handler': self.weeks_tasks},
            3: {'display_text': 'All tasks', 'handler': self.all_tasks},
            4: {'display_text': 'Missed tasks', 'handler': self.missed_tasks},
            5: {'display_text': 'Add task', 'handler': self.add_task},
            6: {'display_text': 'Delete task', 'handler': self.delete_task},
            0: {'display_text': 'Exit', 'handler': self.exterminate}
        }
        self.date_format = '%Y-%m-%d'
        self.state = 'main_menu'
        self.new_task = None

    def display_prompt(self):
        if self.state == 'main_menu':
            for index, menu_option in self.menu_options.items():
                print(f'{index}) {menu_option["display_text"]}')
        elif self.state == 'add_task_menu_description':
            print('Enter task')
        elif self.state == 'add_task_menu_deadline':
            print('Enter deadline')
        elif self.state == 'delete_task_menu':
            print('Chose the number of the task you want to delete:')
            tasks = self.get_all_tasks()
            self.display_tasks(tasks, display_date=True)
        print('> ')

    def user_action(self, action):
        if self.state == 'main_menu':
            try:
                self.menu_options[int(action)]['handler']()
            except (ValueError, KeyError):
                print('Invalid input. Please try again.')
                return
        elif (self.state == 'add_task_menu_description' or
              self.state == 'add_task_menu_deadline'):
            self.add_task(action)
        elif self.state == 'delete_task_menu':
            self.delete_task(action)

    def get_all_tasks(self):
        return self.session.query(Task).all()

    def get_tasks_by_date(self, date):
        return self.session.query(Task).filter(
            Task.deadline == date.strftime(self.date_format)
        ).all()

    def display_tasks(self, tasks, empty_message='Nothing to do!', display_date=False):
        if len(tasks) == 0:
            print(empty_message)
            return
        for index, task in enumerate(tasks, 1):
            print(f'{index}) {task.task}',
                  task.deadline.strftime('%-d %b') if display_date else '')

    def todays_tasks(self):
        today = datetime.now().date()
        tasks = self.get_tasks_by_date(today)

        print('\nToday', today.strftime("%-m %b"))
        self.display_tasks(tasks)
        print('')

    def weeks_tasks(self):
        today = datetime.now().date()

        for day in range(7):
            next_day = today + timedelta(days=day)
            print('\n' + next_day.strftime('%A %-d %b') + ':')
            tasks = self.get_tasks_by_date(next_day)
            self.display_tasks(tasks)
            print('')

    def all_tasks(self):
        tasks = self.get_all_tasks()
        print('\nAll tasks:')
        self.display_tasks(tasks)
        print('')

    def add_task(self, user_input=None):
        if self.state == 'main_menu':
            self.state = 'add_task_menu_description'
        elif self.state == 'add_task_menu_description':
            self.new_task = Task(task=user_input)
            self.state = 'add_task_menu_deadline'
        elif self.state == 'add_task_menu_deadline':
            try:
                deadline = datetime.strptime(user_input, self.date_format)
            except ValueError:
                print('Invalid date format. Date should be in format YYYY-MM-DD')
                return
            self.new_task.deadline = deadline

            self.session.add(self.new_task)
            self.session.commit()

            self.state = 'main_menu'

    def missed_tasks(self):
        today = datetime.now().date()
        tasks = self.session.query(Task).filter(
            Task.deadline < today.strftime(self.date_format)
        ).all()
        print('\nMissed Tasks:')
        self.display_tasks(tasks, empty_message='Nothing is missed!', display_date=True)
        print('')

    def delete_task(self, user_input=None):
        if self.state == 'main_menu':
            self.state = 'delete_task_menu'
        elif self.state == 'delete_task_menu':
            try:
                user_input_int = int(user_input)
                task = self.get_all_tasks()[user_input_int]
            except (ValueError, IndexError):
                print('Invalid input. Please try again!')
                return

            self.session.delete(task)
            self.session.commit()

            print('The task has been deleted!')

            self.state = 'main_menu'

    def exterminate(self):
        print('Bye!')
        sys.exit(0)


todo = ToDo(session)

while True:
    todo.display_prompt()
    action = input().strip()
    todo.user_action(action)
