# KanMind Project – Backend Setup

## Getting Started

# 1. Functionality
User authentication: Management of user accounts and authentication. Task management: Creation, editing and deletion of tasks. API interfaces: Provision of RESTful APIs for interaction with the front end.

# 2. Installation & Setup

## clone respository

git clone git@github.com:Vincent-Goerner/Kanmind-backend.git
cd Kanmind-backend

## create and activate venv

python3 -m venv env

### Mac and Linux:
source env/bin/activate  

### Windows: 
env\Scripts\activate

## install dependencies

pip install -r requirements.txt

## migrate database
python manage.py migrate

## create superuser

python manage.py createsuperuser

## start server

python manage.py runserver

### app is now reachable with http://127.0.0.1:8000/

**Note**  
> This project is intended exclusively for students of the Developer Akademie.  
> It is not licensed for public use or distribution.
