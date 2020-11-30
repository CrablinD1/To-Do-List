from datetime import datetime, timedelta

from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDoList:

    def __init__(self, db_name):
        self.engine = create_engine(
            f'sqlite:///{db_name}.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.menu()

    def menu(self):
        print("1) Today's tasks", "2) Week's tasks", "3) All tasks",
              "4) Missed tasks", "5) Add task", "6) Delete task", "0) Exit",
              sep="\n")
        option = int(input())
        if option == 0:
            exit(1)
        elif option == 1:
            self.show_tasks_today()
        elif option == 2:
            self.show_tasks_week()
        elif option == 3:
            self.show_tasks()
        elif option == 4:
            self.missed_task()
        elif option == 5:
            self.new_task()
        elif option == 6:
            self.delete_task()

    def new_task(self):
        add_task = input('Enter task \n')
        add_deadline = input('Enter a date in YYYY-MM-DD format \n')
        year1, month1, day1 = map(int, add_deadline.split('-'))
        date1 = datetime(year1, month1, day1)
        new_row = Table(task=add_task, deadline=date1)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')
        print('\n')
        return self.menu()

    def show_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print('All tasks:')
        if rows:
            for i in range(len(rows)):
                date = rows[i].deadline
                print('{}. {}. {}'.format(i + 1, rows[i].task,
                                          date.strftime('%d %b')))
        else:
            print('Nothing to do!')
        print('\n')
        return self.menu()

    def show_tasks_today(self):
        today = datetime.today()
        rows = self.session.query(Table).filter(
            Table.deadline == today.date()).order_by(Table.deadline).all()
        print(f"Today {today.strftime('%d %b')}:")
        if rows:
            for i in range(len(rows)):
                print('{}. {}'.format(i + 1, rows[i].task))
        else:
            print('Nothing to do!')
        print('\n')
        return self.menu()

    def show_tasks_week(self):
        today = datetime.today()
        for i in range(0, 7):
            day = today + timedelta(days=i)
            rows = self.session.query(Table).filter(
                Table.deadline == day.date()).order_by(Table.deadline).all()
            print(f"{day.date().strftime('%A')} {day.strftime('%d %b')}:")
            if rows:
                for i in range(len(rows)):
                    print('{}. {}'.format(i + 1, rows[i].task))
            else:
                print('Nothing to do!')
            print('\n')
        return self.menu()

    def missed_task(self):
        today = datetime.today()
        rows = self.session.query(Table).filter(
            Table.deadline < today.date()).order_by(Table.deadline).all()
        print('Missed tasks:')
        if rows:
            for i in range(len(rows)):
                date = rows[i].deadline
                print('{}. {}. {}'.format(i + 1, rows[i].task,
                                          date.strftime('%d %b')))
        else:
            print('Nothing is missed!')
        print('\n')
        return self.menu()

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print('Choose the number of the task you want to delete:')
        if rows:
            for i in range(len(rows)):
                date = rows[i].deadline
                print('{}. {}. {}'.format(i + 1, rows[i].task,
                                          date.strftime('%d %b')))
        else:
            print('Nothing to delete!')
        choice = input()
        specific_row = rows[int(choice) - 1]  # in case rows is not empty
        self.session.delete(specific_row)
        self.session.commit()
        print('The task has been deleted!')
        return self.menu()


new_list = ToDoList('todo')
