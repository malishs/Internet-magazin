## Initial installation of tools and packages
Создание виртуалки и активация [windows].

```sh

python -m venv .venv

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

.venv\Scripts\Activate.ps1

Библиотеки

```sh

pip install django==4.2

pip install django-cleanup

pip install Pillow

pip install djangorestframework

pip install markdown

pip install django-filter

python manage.py runserver 

python manage.py migrate

python manage.py makemigrations
```

Deactivation venv python.

```sh
deactivate

Installing packages used in the project from the list
```sh
python -m pip install -r requirements.txt
```
Basic Django Commands
```sh
python manage.py runserver -> starting django server, Quit the server with CTRL-BREAK
python manage.py migrate -> runs migrations on the database
```