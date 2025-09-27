# KanMind Project – Backend Setup

## Getting Started

# Installation & Setup

## 1. clone respository

git clone git@github.com:Vincent-Goerner/Kanmind-backend.git
cd Kanmind-backend

## 2. create and activate venv

python -m venv env

### Mac and Linux:
source env/bin/activate  

### Windows: 
env\Scripts\activate

## 3. install dependencies

pip install -r requirements.txt

## 4. migrate database

python manage.py makemigrations
python manage.py migrate

## 5. create superuser

python manage.py createsuperuser

## 6. start server

python manage.py runserver

### app is now reachable with http://127.0.0.1:8000/

**Note**  
> This project is intended exclusively for students of the Developer Akademie.  
> It is not licensed for public use or distribution.
