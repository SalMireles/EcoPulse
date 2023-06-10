import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Initializing database...")

conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'))

conn.autocommit = True

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Location;')
cur.execute("""CREATE TABLE Location (
    postal_code VARCHAR(50) NOT NULL,
    longitude FLOAT NOT NULL, 
    latitude FLOAT NOT NULL,
    "state" VARCHAR(50) NOT NULL, 
    city VARCHAR(50) NOT NULL,
    PRIMARY KEY (postal_code));""")

cur.execute('DROP TABLE IF EXISTS Household;')
cur.execute("""CREATE TABLE Household (
    email VARCHAR(255) NOT NULL,
    postal_code VARCHAR(50) NOT NULL,
    household_type VARCHAR(50) NOT NULL,
    on_grid BOOLEAN NOT NULL DEFAULT FALSE,
    square_footage INTEGER NOT NULL,
    thermostat_setting_heating INTEGER,
    thermostat_setting_cooling INTEGER,
    PRIMARY KEY (email),
    FOREIGN KEY (postal_code) REFERENCES Location (postal_code));""")
            
cur.execute('DROP TABLE IF EXISTS HouseholdUtilities;')
cur.execute("""CREATE TABLE HouseholdUtilities (
    email VARCHAR(255) NOT NULL,
    utilities VARCHAR(50) NOT NULL,
    PRIMARY KEY (email, utilities),
    FOREIGN KEY (email) REFERENCES Household (email));""")

cur.execute('DROP TABLE IF EXISTS PowerGenerator;')
cur.execute("""CREATE TABLE PowerGenerator (
    email VARCHAR(255) NOT NULL,
    pg_number BIGSERIAL NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    avg_mon_kilo_hours INTEGER NOT NULL,
    capacity INTEGER,
    PRIMARY KEY (email, pg_number),
    FOREIGN KEY (email) REFERENCES Household(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE);""")
            
cur.execute('DROP TABLE IF EXISTS Manufacturer;')
cur.execute("""CREATE TABLE Manufacturer (
    name VARCHAR(50) PRIMARY KEY);""")
            
cur.execute('DROP TABLE IF EXISTS Appliance;')
cur.execute("""CREATE TABLE Appliance (
    email VARCHAR(255) NOT NULL,
    appliance_number BIGSERIAL NOT NULL,
    manufacturer_name VARCHAR(50) NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    model_name VARCHAR(50),
    BTU_rating INTEGER NOT NULL,
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email) REFERENCES Household(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (manufacturer_name) REFERENCES Manufacturer(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE);""")

cur.execute('DROP TABLE IF EXISTS WaterHeater;')
cur.execute("""CREATE TABLE WaterHeater (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    energy_source VARCHAR(50) NOT NULL, 
    current_temperature INTEGER, 
    capacity NUMERIC(10,1) NOT NULL, 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance(email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE);""")
            
cur.execute('DROP TABLE IF EXISTS HeatPump;')
cur.execute("""CREATE TABLE HeatPump (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    HSPF NUMERIC(10,1) NOT NULL, 
    SEER NUMERIC(10,1) NOT NULL, 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE);""")
            
cur.execute('DROP TABLE IF EXISTS AirConditioner;')
cur.execute("""CREATE TABLE AirConditioner (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    EER NUMERIC(10,1) NOT NULL, 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE);""")
            
cur.execute('DROP TABLE IF EXISTS Heater;')
cur.execute("""CREATE TABLE Heater (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    energy_source VARCHAR(50), 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE);""")

cur.close()
conn.close()

print("Database Initialized")