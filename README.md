# Media Library Rest Full API

## Description

Web site which contains recipes. Authenticated use can create, update, delete is owned recipes He cans also comment and rate others recipes. Anonymous user can only search and see recipes.

Object structure is defined like that :

- User
    - username
    - mail
    - firstname
    - lastname
    - password
    - role

- Recipe
    - title
    - recipe_type
    - difficulty
    - realization_cost
    - preparation_time
    - cooking_time
    - relaxation_time (if necessary)
    - avg_mark (stock avg of marks to avoid computation)
    - *user

- Recipe_step
    - description
    - level (step 1, 2, 3...)
    - *recipe

- RecipePhoto :
    - path
    - *recipe

- Ingredient_family [families](http://www.cuisine-libre.fr/familles-alimentaires)
    - name

- Ingredient_unit_measure (liter, gram, unit...)
    - label

- Ingredient
    - name
    - *ingredient_family
    - *ingredient_unit_measure

- Recipe_ingredient
    - quantity
    - *recipe
    - *ingredient

- Comment
    - text
    - date
    - *user
    - *recipe
    - *comment (if answer)

- Notification
    - date
    - available
    - text (generate from comment or mark)
    - link (necessary to redirect ?)
    - *user
    - *comment (null if mark)
    - *mark (null if comment)


- Mark
    - score
    - *user
    - *recipe


## Installation

## Requirements

You need to have python, pip

```
pip install django django-bootstrap4 django-jquery
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

Note that project uses [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/).

## Licence

[MIT](https://github.com/jbuisine/django-recipes/blob/master/LICENSE)
