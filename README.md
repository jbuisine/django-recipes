# DjangoRecipes

## Description

Web site which contains recipes. Authenticated user can create, update, delete is owned recipes. He can also comment and rate others recipes. Anonymous user can only search and see recipes.

Recipe objects structure is available [here](https://github.com/jbuisine/django-recipes/blob/master/recipes/models.py) and defined like that:

## Installation

## Requirements

You need to have python, pip

```
pip install -r requirements.txt
```

## Configuration

```
python project/manage.py makemigrations
```

```
python project/manage.py migrate
```

Load data fixture
```
python project/manage.py loaddata data_recipes.json
```

## Run server

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

Accounts for testing:

* admin:azerty11 (Admin role which can manage ingredients of recipes...)
* tcaron:azerty11
* agambart:azerty11
* jbuisine:azerty11

## How to contribute ?

This project uses [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/) to improve cooperation during the development.

For each feature, you have to create a new git flow feature branch.

Features to develop are available [here](https://github.com/jbuisine/django-recipes/projects/1). You can choose one you want to do and specify the git branch name associated to it.

Helpful django commands are also available [here](https://github.com/jbuisine/django-recipes/blob/master/COMMANDS.md)

## Model description


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
    - published
    - preparation_time
    - cooking_time
    - relaxation_time (if necessary)
    - mean_of_marks (stock mean of marks to avoid computation each time)
    - number_of_marks (to easily compute new mean with new mark)
    - created_at
    - updated_at
    - published_at
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
    - *recipe

- Recipe_image
    - image
    - created_at
    - *recipe

- Recipe_video
    - path
    - created_at
    - *recipe

- Ingredient_family [families](http://www.cuisine-libre.fr/familles-alimentaires)
    - name

- Ingredient_unit_measure (liter, gram, unit...)
    - label

- Ingredient
    - name
    - *ingredient_family
    - *ingredient_unit_measure

- Ingredient_photo
    - path
    - created_at
    - *ingredient

- Recipe_ingredient
    - quantity
    - *recipe
    - *ingredient
    - *unit_measure (based on unit measure of Ingredient)

- Recipe_comment
    - text
    - date
    - *user
    - *recipe
    - *comment (if answer, not working for the moment)

- Notification
    - date
    - available
    - text (generate from comment or mark)
    - link (necessary to redirect ?)
    - *user
    - *comment (null if mark)
    - *mark (null if comment)


- Recipe_mark
    - mark_score
    - *user
    - *recipe

## Contributors

* [tcaron](https://github.com/tcaron)
* [AlexandreGambart](https://github.com/AlexandreGambart)
* [jbuisine](https://github.com/jbuisine)

## Licence

[MIT](https://github.com/jbuisine/django-recipes/blob/master/LICENSE)
