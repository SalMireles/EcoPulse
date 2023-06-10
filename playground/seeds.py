from data import (AIR_CONDITIONER, APPLIANCE, HEAT_PUMP, HEATER,
                  HOUSEHOLD_DATA, HOUSEHOLD_UTILITIES, LOCATION_DATA,
                  MANUFACTURER, POWER_GENERATOR, WATER_HEATER)


def seed_manufacturer_table(connection):
    sql_command = "INSERT INTO Manufacturer (name) VALUES (%s)"

    # Add data then close the connection
    cursor = connection.cursor()
    for data in MANUFACTURER:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_location_table(connection):
    sql_command = (
        "INSERT INTO Location ("
        "postal_code, "
        "longitude, "
        "latitude, "
        "state, "
        "city"
        ") "
        "VALUES (%s, %s, %s, %s, %s)"
    )

    # Add data
    cursor = connection.cursor()
    for data in LOCATION_DATA:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_household_table(connection):
    sql_command = (
        "INSERT INTO Household ("
        "email, "
        "postal_code, "
        "household_type, "
        "on_grid, "
        "square_footage, "
        "thermostat_setting_heating, "
        "thermostat_setting_cooling"
        ") "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in HOUSEHOLD_DATA:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_household_utilities_table(connection):
    sql_command = (
        "INSERT INTO HouseholdUtilities (" "email, " "utilities" ") " "VALUES (%s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in HOUSEHOLD_UTILITIES:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_power_generator_table(connection):
    sql_command = (
        "INSERT INTO PowerGenerator ("
        "email, "
        "pg_number, "
        "type, "
        "avg_mon_kilo_hours, "
        "capacity"
        ") "
        "VALUES (%s, %s, %s, %s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in POWER_GENERATOR:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_appliance_table(connection):
    sql_command = (
        "INSERT INTO Appliance ("
        "email, "
        "appliance_number, "
        "manufacturer_name, "
        "type, "
        "model_name, "
        "BTU_rating"
        ") "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in APPLIANCE:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_water_heater_table(connection):
    sql_command = (
        "INSERT INTO WaterHeater ("
        "email, "
        "appliance_number, "
        "energy_source, "
        "current_temperature, "
        "capacity"
        ") "
        "VALUES (%s, %s, %s, %s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in WATER_HEATER:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_heat_pump_table(connection):
    sql_command = (
        "INSERT INTO HeatPump ("
        "email, "
        "appliance_number, "
        "HSPF, "
        "SEER"
        ") "
        "VALUES (%s, %s, %s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in HEAT_PUMP:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_air_conditioner_table(connection):
    sql_command = (
        "INSERT INTO AirConditioner ("
        "email, "
        "appliance_number, "
        "EER"
        ") "
        "VALUES (%s, %s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in AIR_CONDITIONER:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()


def seed_heater_table(connection):
    sql_command = (
        "INSERT INTO Heater ("
        "email, "
        "appliance_number, "
        "energy_source"
        ") "
        "VALUES (%s, %s, %s)"
    )

    # Add data then close the connection
    cursor = connection.cursor()
    for data in HEATER:
        cursor.execute(sql_command, data)

    connection.commit()
    cursor.close()
