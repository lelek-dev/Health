# Health

Simple webapplication to manage and share presonal wishes

### REQUIREMENTS

##### Running in Docker

* Docker

##### Running locally

* Django Installation
* Python installation with all packages (requirements.txt)
* PostgresDB

### Getting Started

##### Running in Docker

1. Create /health/.env File and modify content
2. run "docker-compose build"
3. run "docker-compose up"

##### Running locally

1. Create /health/.env File and modify content
2. If database is not set up yet:
   1. python manage.py makemigrations
   2. python manage.py migrate
3. python manage.py runserver

### Structure

/health contains main configuration
/externalAuth contains domain for authentication with external identification provider
/internalAuth contains domain for registration, login, ...
/healthRecords contains domain for lists and wishes
/docotr contains domain for actions performed by doctors
/static contains static files such as images, css and js
