# DjangoRecipes

## Description

Web site which contains recipes. Authenticated user can create, update, delete is owned recipes. He can also comment and rate others recipes. Anonymous user can only search and see recipes.

Recipe objects structure is available [here](https://github.com/jbuisine/django-recipes/blob/master/recipes/models.py) and defined like that:

- User
    - username
    - mail
    - firstname
    - lastname
    - password
    - role

- Recipe
    - title
    - realization_cost
    - preparation_time
    - cooking_time
    - relaxation_time (if necessary)
    - mean_of_marks (stock mean of marks to avoid computation each time)
    - number_of_marks (to easily compute new mean with new mark)
    - *recipe_type
    - *difficulty
    - *user

- Recipe_difficulty
    - label
    - level

- Recipe_type
    - label

- Recipe_step
    - description
    - level (step 1, 2, 3...)
    - *recipe

- Recipe_media
    - path
    - date
    - *recipe
    - *media_type

- Media_type
    - label

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
    - mark_score
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

## How to contribute ?

This project uses [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/) to improve cooperation during the development.

For each feature, you have to create a new git flow feature branch.

Features to develop are available [here](https://github.com/jbuisine/django-recipes/projects/1). You can choose one you want to do and specify the git branch name associated to it.

Helpful django commands are also available [here](https://github.com/jbuisine/django-recipes/blob/master/COMMANDS.md)

## Contributors

* [tcaron](https://github.com/tcaron)
* [AlexandreGambart](https://github.com/AlexandreGambart)
* [jbuisine](https://github.com/jbuisine)

## Licence

[MIT](https://github.com/jbuisine/django-recipes/blob/master/LICENSE)
