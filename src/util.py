import os

import psycopg2
from dotenv import load_dotenv
from flask import g

# Load environment variables
load_dotenv()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """

    if not hasattr(g, 'psql_conn'):
        g.psql_conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'))
        
        g.psql_conn.autocommit = True

    return g.psql_conn

def valid_postal_code(postal_code):
    return True

def valid_search_radius(radius):
    return True

def valid_search_term(search_term):
    return True
