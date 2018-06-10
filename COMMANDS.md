# Commands

## Create project
django-admin startproject masterI2L

## How to run
python manage.py runserver

## Create apps
python manage.py startapp xxxx

# DataBase
python manage.py migrate

## activate models and create it in database
python manage.py makemigrations

## execute migrations
python manage.py migrate

## get access to db
sqlite3 xxx.db
.tables
.help

## show sql commands run
python manage.py sqlmigrate polls 0001

# Manage application in CLI

## Run shell
python manage.py shell

## Show manage of a Model
: Question.objects

## Create new object
: q = Question()
: q.label = "Your question here!"
: q.date = '2018-01-01'
: q.save()
: q.pk

## Read history of request
: from django.db import connection
: connection.queries_log

## Use entity manager
Question.objects.count()
Question.objects.all()
Question.objects.filter(id=1)

### use of look up
Question.objects.filter(label__startswith='Q')

### execute query directly
Question.objects.get(id=1)

### use of Q
from django.db.models import Q
Q(id=1) | Q(id=2)

### loop query set result
for q in qs:
    print(q.label)

### refresh object from database
q.refresh_from_db()

### other useful function
Question.objects.get_or_create
Question.objects.update_or_create
Question.objects.first
Question.objects.exists
Question.objects.exclude

### use only and defer
only : specify fields of the object we want
defer : specify fields of the object we do not want

## Display object
q.__str__()

## manage association
Choice.objects.create(question_id=1, label="Choice", votes=0)

q.choice_set
q.choice_set.all()

Choice.objects.select_related('question').all()
Choice.objects.prefetch_related('choice').all()
Question.objects.prefetch_related()

# Project structure

## Notes
*urls.py* contains Routes (we can separate routes by project)
