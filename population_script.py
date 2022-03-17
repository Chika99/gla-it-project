import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pickee_project.settings')
import django

django.setup()
import datetime
from api.models import (User, Session)

users = [
    {'email': 'rhys@email.com', 'password': 'rhyspassword', 'first_name': 'Rhys', 'last_name': 'Stephens',
     'gender': 'MALE', 'age': 23},
    {'email': 'pedro@email.com', 'password': 'pedropassword', 'first_name': 'Pedro', 'last_name': 'Belfort',
     'gender': 'MALE', 'age': 42},
    {'email': 'nathan@email.com', 'password': 'nathanpassword', 'first_name': 'Nathan', 'last_name': 'Schneddy',
     'gender': 'MALE', 'age': 23},
    {'email': 'anton@email.com', 'password': 'antonpassword', 'first_name': 'Anton', 'last_name': 'Samoilov',
     'gender': 'MALE', 'age': 19},
    {'email': 'julia@email.com', 'password': 'juliapassword', 'first_name': 'Julia', 'last_name': 'Saari',
     'gender': 'FEMALE', 'age': 10},
    {'email': 'kate@email.com', 'password': 'katepassword', 'first_name': 'Kate', 'last_name': 'Hickey',
     'gender': 'FEMALE', 'age': 35},
    {'email': 'meredith@email.com', 'password': 'meredithpassword', 'first_name': 'Meredith', 'last_name': 'Ellington',
     'gender': 'FEMALE', 'age': 7},
    {'email': 'mark@email.com', 'password': 'markpassword', 'first_name': 'Mark', 'last_name': 'Morrison',
     'gender': 'MALE', 'age': 28},
    {'email': 'hugh@email.com', 'password': 'hughpassword', 'first_name': 'Hugh', 'last_name': 'Winchester',
     'gender': 'MALE', 'age': 72},
    {'email': 'gareth@email.com', 'password': 'garethpassword', 'first_name': 'Gareth', 'last_name': 'Sears',
     'gender': 'MALE', 'age': 54},
    {'email': 'chris@email.com', 'password': 'chrispassword', 'first_name': 'Chris', 'last_name': 'Castaldo',
     'gender': 'MALE', 'age': 14}
]


sessions = [
    {'users': {'rhys@email.com', 'pedro@email.com'}},
    {'users': {'rhys@email.com', 'pedro@email.com', 'nathan@email.com', 'anton@email.com'}},
    {'users': {'nathan@email.com'}},
    {'users': {'nathan@email.com', 'anton@email.com'}},
    {'users': {'julia@email.com', 'kate@email.com', 'meredith@email.com'}},
    {'users': {'mark@email.com', 'gareth@email.com', 'hugh@email.com', 'chris@email.com'}}
]


def populate():
    User.objects.create_superuser('admin', 'admin321')

    for user in users:
        add_user(user['email'], user['password'], user['first_name'], user['last_name'], user['gender'], user['age'])


def add_user(email, password, first_name, last_name, gender, age):
    user = User.objects.create_user(email=email,
                                          password=password,
                                          first_name=first_name,
                                          last_name=last_name,
                                          gender=gender,
                                          age=age)


def add_session(users):
    session = Session.objects.create()
    for user_email in users:
        session.users.add(User.objects.get(email=user_email))


if __name__ == '__main__':
    print('Starting population script...')
    populate()
    print('Pickee has been populated!')
