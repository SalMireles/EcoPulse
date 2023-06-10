import os

import psycopg2
from dotenv import load_dotenv

from seeds import (
    seed_air_conditioner_table,
    seed_appliance_table,
    seed_heat_pump_table,
    seed_heater_table,
    seed_household_table,
    seed_household_utilities_table,
    seed_location_table,
    seed_manufacturer_table,
    seed_power_generator_table,
    seed_water_heater_table,
)

# Load environment variables
load_dotenv()


def db_connection():
    """Connect to local postgres database and return a connection object."""
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return connection


def delete_all_table_data():
    """Removes all data from all tables."""
    connection = db_connection()
    cursor = connection.cursor()
    # Order matters due to foreign key constraints
    tables = [
        "Manufacturer",
        "HouseholdUtilities",
        "Household",
        "Location",
        "PowerGenerator",
        "Appliance",
        "WaterHeater",
        "HeatPump",
        "AirConditioner",
        "Heater",
    ]
    for table_name in tables:
        cursor.execute(f"DELETE FROM {table_name}")

    connection.commit()
    cursor.close()


def main():
    """Seed all tables with data."""
    # Delete and start over
    delete_all_table_data()

    print("Seeding database...")

    # Seed all data
    connection = db_connection()
    seed_manufacturer_table(connection)
    seed_location_table(connection)
    seed_household_table(connection)
    seed_household_utilities_table(connection)
    seed_appliance_table(connection)
    seed_water_heater_table(connection)
    seed_heat_pump_table(connection)
    seed_air_conditioner_table(connection)
    seed_heater_table(connection)
    seed_power_generator_table(connection)
    # Close the connection
    connection.close()

    print("Seeding complete")


if __name__ == "__main__":
    main()
