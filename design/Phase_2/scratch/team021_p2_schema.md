**Phase 2 CREATE TABLE STATEMENTS** | CS 6400 - Spring 2023 | **Team 021**

## NOTE: This is a draft file. I have added notes to each table to describe why I did what I did. In the final revision, I think we may need to submit only the create database and create table statements, such that it can all be called and executed at once. Can discuss.
___

## Table of Contents
**Create Database Statement** [Create Database Statement](#Create-Database-Statement)

**Location Relation** [Location](#Location-Relation)

**Household Relation** [Household](#Household-Relation)

**On-grid Household Utilities Relation** [HouseholdUtilities](#HouseholdUtilities)

**Power Generator Relation** [PowerGenerator](#Power-Generator-Relation)

**Manufacturer Relation** [Manufacturer](#Manufacturer-Relation)

**Appliance Relation** [Appliance](#Appliance-Relation)

**Water Heater Relation** [WaterHeater](#Water-Heater-Relation)

**Heat Pump Relation** [HeatPump](#Heat-Pump-Relation)

**Air Conditioner Relation** [AirConditioner](#Air-Conditioner-Relation)

**Heater Relation** [Heater](#Heater-Relation)


# Create Database Statement
I did not create users for this project. I simply created a database and used the default user. As part of this, I did not grant any special permissions. I updated some collate and ctype settings IAW the example schema. 

The following statement was used to create the database and was tested in postgres. 

```sql
DROP DATABASE IF EXISTS cs6400_sp23_team021;
CREATE DATABASE cs6400_sp23_team021
    ENCODING 'UTF8'
    LC_COLLATE 'en_US.utf8'
    LC_CTYPE 'en_US.utf8'
    TEMPLATE template0;
\c cs6400_sp23_team021
```

# Location Relation: 
Forms the 1-side of the N-1 relation with household. This relation will contain only it’s attributes. Postal_code will be referenced by the Household relations. Location table has to be created before the household table is created.

### CREATE LOCATION TABLE STATEMENT
```sql
CREATE TABLE Location (
    postal_code VARCHAR(50) NOT NULL,
    longitude FLOAT NOT NULL, 
    latitude FLOAT NOT NULL,
    "state" VARCHAR(50) NOT NULL, 
    city VARCHAR(50) NOT NULL,
    PRIMARY KEY (postal_code)
); 
```

# Household Relation:
We have household with mandatory disjoint for on-grid or off-grid. Based on the mandatory disjoint, I have set up three relations (see CASE STUDY 1 and CASE STUDY 4 lecture video). The relation also forms the N-side of the the N-1 relationship with location.

### CREATE ON-GRID HOUSEHOLD TABLE STATEMENT
```sql
CREATE TABLE Household (
    email VARCHAR(255) NOT NULL,
    postal_code VARCHAR(50) NOT NULL,
    household_type VARCHAR(50) NOT NULL,
    on_grid BOOLEAN NOT NULL DEFAULT FALSE,
    square_footage INTEGER NOT NULL,
    thermostat_setting_heating INTEGER,
    thermostat_setting_cooling INTEGER,
    PRIMARY KEY (email),
    FOREIGN KEY (postal_code) REFERENCES location (postal_code)
);
```


# HouseholdUtilities:

### CREATE ON-GRID HOUSEHOLD UTILITIES TABLE STATEMENT
```sql
CREATE TABLE HouseholdUtilities (
    email VARCHAR(255) NOT NULL,
    utilities VARCHAR(50) NOT NULL,
    PRIMARY KEY (email, utilities),
    FOREIGN KEY (email) REFERENCES household (email)
);
```


# Power Generator Relation: 
The power generator relation is a weak entity type, which is required for off-grid households. The primary key is a composite key of email and pg_number. Email is also a foreign key referencing the Household relation. The CASCADE clauses simply update the relation in case the names in the Household relations get updated or are deleted. 

### CREATE POWER GENERATOR TABLE STATEMENT
```sql
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
```

# Manufacturer Relation:
This relation will contain only it’s attributes as it is the 1 side of an N-1 relation. Manufacturer needs to be created before the Appliance relation is created.

### CREATE MANUFACTURER TABLE STATEMENT
```sql
CREATE TABLE Manufacturer (
    name VARCHAR(50) PRIMARY KEY
);
```

# Appliance Relation:
This relation contains its attributes, with a primary key being the composite key of email and appliance_number. Email is also a foreign key referencing the Household relation. The CASCADE clauses simply update the relation in case the names in the Household relations get updated or are deleted. Manufacturer name is also a foreign key referencing the Manufacturer relation. The CASCADE clauses simply update the relation in case the names in the Manufacturer relations get updated or are deleted.

### CREATE APPLIANCE TABLE STATEMENT
```sql
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
```

# Water Heater Relation:
This relation contains its attributes, with a primary key being the composite key of email and appliance_number. Email and appliance_number are also foreign keys referencing the appliance relation. The CASCADE clauses simply update the relation in case the names in the appliance relations get updated or are deleted.


### CREATE WATER HEATER TABLE STATEMENT
```sql
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
```


# Heat Pump Relation:
This relation contains its attributes, with a primary key being the composite key of email, appliance_number. Email, appliance_number are also foreign keys referencing the Appliance relation. The CASCADE clauses simply update the relation in case the names in the Appliance relations get updated or are deleted. HSPF and SEER are the attributes of the heat pump relation.


### CREATE HEAT PUMP TABLE STATEMENT
```sql
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
```


# Air Conditioner Relation:
This relation contains its attributes, with a primary key being the composite key of email, appliance_number. Email, appliance_number are also foreign keys referencing the Appliance relation. The CASCADE clauses simply update the relation in case the names in the Appliance relations get updated or are deleted. EER is the attribute of the heat pump relation.

### CREATE AIR CONDITIONER TABLE STATEMENT
```sql
CREATE TABLE AirConditioner (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    EER NUMERIC(10,1) NOT NULL, 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```


# Heater Relation:
This relation contains its attributes, with a primary key being the composite key of email, appliance_number. Email, appliance_number are also foreign keys referencing the Appliance relation. The CASCADE clauses simply update the relation in case the names in the Appliance relations get updated or are deleted. Energy source is the attribute of the heat pump relation.


### CREATE HEATER TABLE STATEMENT
```sql
CREATE TABLE Heater (
    email VARCHAR(255) NOT NULL,
    appliance_number INTEGER NOT NULL,
    energy_source VARCHAR(50), 
    PRIMARY KEY (email, appliance_number),
    FOREIGN KEY (email, appliance_number) REFERENCES Appliance (email, appliance_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```



























