# Parcel locker project.
### This is a microservice application that offers functionalities of a parcel locker


## Table of Contents

* [General Info](#general-information)
* [Quick Setup](#quick-setup)
* [Development Setup](#development-setup)
  * [Virtual environment](#virtual-environment)
  * [Docker Setup](#docker-setup)
  * [Migrations](#migrations)
  * [Tests](#tests)
* [Technologies](#technologies)
* [Features](#features)
* [Usage](#usage)
* [Project Status](#project-status)


## General information
The purpose of this project is to present several
different patterns of good programming practices and
implement them in a microservice web application.

## Quick Setup
Watch the video:
------- TODO TU DODAJ LINK -------

Or follow instructions below :
  1. Get into the directory of the project where docker-compose.yml exists.
  2. Run command:
  > docker-compose up -d --build


## Development Setup
Watch the video:
------- TODO TU DODAJ LINK -------

Or follow instructions below:

### Virtual environment
This project has separate virtualenvs for each of the app.
It is important to create it that way to avoid dependency conflicts.
You must enter commands listed below in each of the app directories.
When you are placed in tha app directory, run:

> pipenv shell

> pipenv install

Remember to repeat these steps in both applications!


### Docker setup
In order to containerize this project, run the 
following commands in the main project directory:

> docker-compose -f docker-compose-dev.yml up -d --build

For the logs to appear in console, enter:

> docker-compose -f docker-compose-dev.yml logs -f

If you want to stop the running container, while in the project directory
enter command:

> docker-compose -f docker-compose-dev.yml stop


### Migrations
Next step in project configuration is to run the migration scripts.
However, it may not be possible from the app directory, since everything
got created inside the container. So we have to execute migration commands
inside the app container. In order to do it, we need to know
container id. To find out what the id is run the command inside the project
directory:

> docker ps -a

Find out the container name corresponding to the app and next to it,
you will find the CONTAINER_ID. Next, execute the following command to get inside 
the app container (in the CONTAINER_ID place you can type just the first
three symbols of the ID):

> docker exec -it <CONTAINER_ID> bash

You can now run the following migration scripts 
For the main database:

> alembic upgrade head

For the test database:

> alembic -x test=true upgrade head

Remember to repeat these steps in both parcel-locker-app and customers app!

### Tests
While being inside the container execute the following command:
> pipenv run pytest

At this point all the tests should pass with a PASSED result.

Remember to repeat these steps in both parcel-locker-app and customers app!

### Postman
(Optional) Postman installation for easily running routes.
For the Flask routes, it is recommended to use Postman as it is much
easier and more intuitive than running routes from the browser.
This app has the routes already provided. All you have to do is import
the Postman json collection.


## Technologies
- Python 3.12
- Flask
- pytest
- Docker
- pipenv
- MySQL
- SQLAlchemy
- alembic
- Git

## Features
- Flask framework used for web
- Micro service structure
- Included Postman json file with routes to import
- Implementation of abstract factory design pattern
- Database migrations with alembic
- ORM with the use of SQLAlchemy
- Tests for every project layer
- Entire project containerized with Docker
- Virtual environment managed with pipenv

## Usage
This project is being made for usage only as a standalone application 
and has no other use cases other than presented in this document.

## Project Status
Project is: in progress.
