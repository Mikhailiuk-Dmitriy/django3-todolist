# django3-todolist

My graduation Python project

This web application is a task management tool. The app allows you to create a to-do list, add new tasks, delete and edit them. 
You can also use the API to make necessary changes to the app.

Dependencies:

-Python 3.10

-Poetry

Installation:

-download this repository

-download the .env file and move it to the root of the project (file name must start with a dot)   https://cloud.mail.ru/public/1Ndk/1P9uWVMfV

-in this repository via cmd run: "poetry install"

-"poetry run python manage.py migrate"

-"poetry run python manage.py runserver"

Main ways to work with the API:

-api/v1/auth/users/  method POST user registration

-auth/token/login/ method POST user authorization and receiving a token

-api/v1/todolist/ method GET  returns all data 

-api/v1/todolist/ method POST creates todo

-api/v1/todolist/<int:pk>/ method GET  details todo

-api/v1/todolist/<int:pk>/ method PUT updates todo

-api/v1/todolist/<int:pk>/ method DELETE deletes todo

Languages: Python, HTML, CSS.

Frameworks: Django, Django REST, Bootstrap.

Database: SQLite3
