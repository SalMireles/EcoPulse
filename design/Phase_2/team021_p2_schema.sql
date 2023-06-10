-- This was tested on Postgres 13.4.
-- It is likely compatible with any relatively recent Postgres version.

DROP DATABASE IF EXISTS cs6400_sp23_team021;
CREATE DATABASE cs6400_sp23_team021
    ENCODING 'UTF8'
    LC_COLLATE 'en_US.utf8'
    LC_CTYPE 'en_US.utf8'
    TEMPLATE template0;

CREATE TABLE Location (
    postal_code VARCHAR(50) NOT NULL,
    longitude FLOAT NOT NULL, 
    latitude FLOAT NOT NULL,
    "state" VARCHAR(50) NOT NULL, 
    city VARCHAR(50) NOT NULL,
    PRIMARY KEY (postal_code)
); 

CREATE TABLE Household (
    email VARCHAR(255) NOT NULL,
    postal_code VARCHAR(50) NOT NULL,
    household_type VARCHAR(50) NOT NULL,
    on_grid BOOLEAN NOT NULL DEFAULT FALSE,
    square_footage INTEGER NOT NULL,
    thermostat_setting_heating INTEGER,
    thermostat_setting_cooling INTEGER,
    PRIMARY KEY (email),
    FOREIGN KEY (postal_code) REFERENCES Location (postal_code)
);

CREATE TABLE HouseholdUtilities (
    email VARCHAR(255) NOT NULL,
    utilities VARCHAR(50) NOT NULL,
    PRIMARY KEY (email, utilities),
    FOREIGN KEY (email) REFERENCES Household (email)
);

CREATE TABLE PowerGenerator (
    email VARCHAR(255) NOT NULL,
    pg_number BIGSERIAL NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    avg_mon_kilo_hours INTEGER NOT NULL,
    capacity INTEGER,
    PRIMARY KEY (email, pg_number),
    FOREIGN KEY (email) REFERENCES Household(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Manufacturer (
    name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Appliance (
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
        ON UPDATE CASCADE 
);

CREATE TABLE WaterHeater (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    energy_source VARCHAR(50) NOT NULL, 
    current_temperature INTEGER, 
    capacity NUMERIC(10,1) NOT NULL, 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance(email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE HeatPump (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    HSPF NUMERIC(10,1) NOT NULL, 
    SEER NUMERIC(10,1) NOT NULL, 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE AirConditioner (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    EER NUMERIC(10,1) NOT NULL, 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Heater (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    energy_source VARCHAR(50), 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);