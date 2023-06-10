# Project Setup

## 1. Install Postgres, Python, IDE

If you are missing any of these, see Detailed Installation Instructions below.

## 2. Create the Postgres database

`sudo -iu postgres`

`createdb cs6400_sp23_team021`

`exit`

## 3. Create Virtual Environment for Project (Recommended)

From project root directory:

`python -m venv venv`

Activate it:

`. venv/bin/activate`

## 4. Install Dependencies

`python -m pip install -r requirements.txt`

## 5. Add .env file with your Postgres Info

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cs6400_sp23_team021
DB_USER=postgres
DB_PASSWORD=password
```

Flask app currently runs on port 5000, so make sure Postgres port is different.

## 6. Initialize the Database

This drops and recreates all tables:

From project 'db' folder:

`python init_db.py`

From the usage examples I've seen, psycopg2 connects to a database before allowing you to perform operations - so you can't really use
it to drop the database.

If you'd like to entirely drop and re-create the database, see "Tips" below.

## 7. Seed the Database

This adds the test data to all the tables.

From project 'seeds' folder:

`python seed_db.py`

This will take about 10 seconds.

## 8. Run the App in Development Mode

From project root directory:

`flask run --debug`

The app will automatically reload if code changes, and show an interactive debugger on error.

## 9. View Data

Visit any of the following routes to see some of Sal's great seed data!

```
http://127.0.0.1:5000/appliances
http://127.0.0.1:5000/power-generation
http://127.0.0.1:5000/reports/manufacturers
http://127.0.0.1:5000/reports/manufacturers/Man1
http://127.0.0.1:5000/reports/hcm
http://127.0.0.1:5000/reports/water-heaters
http://127.0.0.1:5000/reports/water-heaters/AK
http://127.0.0.1:5000/reports/off-grid
```

<br>

## Tips

### Postgres Interactive Console

`sudo -iu postgres`

`psql`

Connect to the project database:

`\c cs6400_sp23_team021`

List tables:

`\dt`

You can write SQL as well, and press return for line breaks.  Remember to terminate the command with `;`:

`select * from airconditioner;`

Exit:

`\q`

`exit`

Drop and re-create a database:

`sudo -iu postgres`

`dropdb cs6400_sp23_team021`

`createdb cs6400_sp23_team021`

<br>


# Detailed Installation Instructions

## Python

Download the latest Python (Mac/Linux probably already have it):

https://www.python.org/downloads/

This Python installer should come with Pip (package manager), if not:

`python -m ensurepip --upgrade`

<br>

## Virtual Environment

Create the virtual environment:

`python -m venv venv`

Activate it:

`. venv/bin/activate`

Resource

https://docs.python.org/3/library/venv.html

<br>

## Postgres

### Install & Configure Postgres (Linux)

If you're using Mac it's probably similar:

`sudo apt update`

`sudo apt install postgresql postgresql-contrib`

`sudo systemctl start postgresql.service`

### Start Postgres from Terminal

`sudo -iu postgres`

Change the admin password to 'password' (may not be necessary):

`\password`

```
postgres=# \password
Enter new password:
Enter it again:
postgres=#
```

To Exit Postgres:

`\q`

`exit`

Create the database:

`sudo -iu postgres createdb cs6400_sp23_team021`

### Resources

Postgres Installation:

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04

Flask Specific:

https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application

<br>

## IDE

VSCode is a good option:

https://code.visualstudio.com/

Then, from the project directory:

`code .`

Inside the IDE it may prompt you to install extensions for Python, you can do this.