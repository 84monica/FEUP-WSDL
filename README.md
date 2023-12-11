# FEUP-WSDL
## Set Up

```python
python3 manage.py sqlmigrate backend 0001
python3 manage.py makemigrations backend
python3 manage.py migrate
python3 manage.py extract_data
```

## How to run

```python
python3 manage.py runserver
```

HomePage is at /globalbite