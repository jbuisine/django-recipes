# Media Library Rest Full API

## Description

Web site which contains recipes. Authenticated use can create, update, delete is owned recipes He cans also comment and rate others recipes. Anonymous user can only search and see recipes.

Object structure is defined like that :

// TODO add objects relationships

## Installation

## Requirements

You need to have python, pip

```
pip install django django-bootstrap3 django-jquery
```

## Configuration

```
python project/manage.py makemigrations core
```

```
python project/manage.py migrate core && python project/manage.py migrate
```

Create your new user :

```
python project/manage.py createsuperuser
```

And then, run the server :

```
python project/manage.py runserver
```

or if you want to precise a specific port number :

```
python project/manage.py runserver 8080
```

## Utilisation

The default server address is [http://localhost:8000](http://localhost:8000)


## Contributors

* [tcaron](https://github.com/tcaron)
* [AlexandreGambart](https://github.com/AlexandreGambart)
* [jbuisine](https://github.com/jbuisine)

## Licence

[MIT](https://github.com/jbuisine/django-recipes/blob/master/LICENSE)
