
## Seeding the database with sample data

### Prerequisites
* Python 3.10.0
* pyenv (recommended)
* SQLTools (vscode plugin)
* .env file with database credentials
```python
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cs6400
DB_USER=postgres
DB_PASSWORD=topsecret
```
### Installation
* pip install -r requirements.txt

### Usage
1. Create database and tables using team021_p2_schema.sql from phase 2
   1. In VScode, I had to first drop existing database, create database, then create tables. Also, `'en_US.utf8'` had to be changed to `'en_US.UTF-8'`
   2. It may be faster to drop the database in pgAdmin4 or in the console
2. Add sample data to `data.py` (or skip if using existing data)
3. Run ```python seed_database.py```
4. View results in SQLTools table
5. Test queries such as (remember to use single quotes for strings eval):
 ```sql
 SELECT COUNT(email) FROM household WHERE email = 'john@example.com';
 ```