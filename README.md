# FEUP-WSDL

## How to run

```
python3 manage.py runserver
```

HomePage is at /polls

## Populate Model

```
python3 manage.py sqlmigrate polls 0001
python3 manage.py makemigrations polls
python3 manage.py migrate
python3 manage.py extract_data
```