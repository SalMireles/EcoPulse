import pathlib

import pandas as pd

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()


def get_postal_codes():
    """Imports postal code data from a csv and formats it to pass into a sql
    insert.
    """
    # Define the column names and types
    column_names = ["zip", "city", "state", "lat", "lon"]
    column_types = {"zip": str, "city": str,
                    "state": str, "lat": float, "lon": float}

    df = pd.read_csv(f"{CURRENT_DIR}/postal_codes.csv",
                     names=column_names, skiprows=1)

    # Order data and assign type
    column_order = ["zip", "lon", "lat", "state", "city"]
    df = df.reindex(columns=column_order)
    df = df.astype(column_types)

    # Return the data to a list of tuples
    return [tuple(x) for x in df.values]


LOCATION_DATA = get_postal_codes()

_EMAILS = [
    "john@example.com",
    "jane@example.com",
    "sal@example.com",
    "tim@example.com",
    "jerry@example.com",
] + [f'{i}@example.com' for i in range(6, 30)]

# Email, zip, household_type, ongrid, sqrft, heating(F), cooling(F)
HOUSEHOLD_DATA = [
    (_EMAILS[0], "71937", "house", True, 750, 100, 50),
    (_EMAILS[1], "72044", "apartment", True, 1500, 80, 45),
    (_EMAILS[2], "56171", "townhome", False, 1200, 70, 45),
    (_EMAILS[3], "49430", "condominium", True, 1100, 60, 35),
    (_EMAILS[4], "52585", "mobile_home", False, 600, 50, 25),
    (_EMAILS[5], "52585", "house", False, 600, 50, 25),
]

# Email, utilities (Electric, Gas, Steam, Fuel Oil)
HOUSEHOLD_UTILITIES = [
    (_EMAILS[0], "Fuel Oil"),
    (_EMAILS[1], "Electric"),
    (_EMAILS[2], "Steam"),
    (_EMAILS[3], "Gas"),
    (_EMAILS[4], "Electric"),
]

# Email, appliance#, manuf name, type, model name, BTU rating
# type = Water heater or Air Handler
APPLIANCE = [
    (_EMAILS[0], 1, "Man1", "Water Heater", "Mod_a", 1540),
    (_EMAILS[0], 2, "Man1", "Air Handler", "Man", 1500),
    (_EMAILS[0], 3, "Man1", "Water Heater", "WH2", 3000),
    (
        _EMAILS[1],
        1,
        "Man2",
        "Air Handler",
        "Mod_b",
        1000,
    ),
    (
        _EMAILS[1],
        2,
        "Man2",
        "Water Heater",
        "WH1",
        1200,
    ),
    (
        _EMAILS[2],
        1,
        "Man3",
        "Air Handler",
        "Mod_c",
        1000,
    ),
    (
        _EMAILS[3],
        1,
        "Man4",
        "Air Handler",
        "Mod_d",
        1500,
    ),
    (
        _EMAILS[4],
        1,
        "Man5",
        "Air Handler",
        "Mod_e",
        1600,
    ),
    (
        _EMAILS[4],
        2,
        "Man5",
        "Air Handler",
        "Mod_e",
        1600,
    ),
    (
        _EMAILS[4],
        3,
        "Man5",
        "Air Handler",
        "Mod_e",
        1600,
    ),
    (
        _EMAILS[4],
        4,
        "Man5",
        "Air Handler",
        "Mod_e",
        1600,
    ),
]

# Email, appliance#, energy source, current temp, capacity (gallons)
# Source heat pump is not the same as air handler
# Energy Source: Electric, Gas, Thermosolar, or Heat Pump
WATER_HEATER = [
    (_EMAILS[0], 1, "Heat Pump", 75, 122.5),
    (_EMAILS[1], 2, "Electric", 100, 140.5),
    (_EMAILS[0], 3, "Heat Pump", None, 140.5),
]

# Email, appliance#, HSPF (~8.0-10.0), SEER (~12.0-23.5)
HEAT_PUMP = [
    (_EMAILS[0], 2, 8.0, 12.0),
    (_EMAILS[4], 1, 8.0, 12.0),
]

# Email, appliance#, EER (2.2-3.3)
AIR_CONDITIONER = [
    (_EMAILS[3], 1, 2.5),
    (_EMAILS[4], 1, 2.5),
]

# Email, appliance#, energy source
# Energy Source: Electric, Gas, Thermosolar, or Heat Pump
HEATER = [
    (_EMAILS[2], 1, "Gas"),
    (_EMAILS[4], 1, "Thermosolar"),
    (_EMAILS[4], 2, "Thermosolar"),
    (_EMAILS[4], 3, "Gas"),
    (_EMAILS[4], 4, "Heat Pump"),
]

# Email, pg_number, type, avg_mon_kilo_hours (50-500), capacity (10-100)
# Type: Solar-Electric-electric, Wind
# Offgrid Mandatory
# Can have multiple with optional batter capacity
POWER_GENERATOR = [
    (_EMAILS[2], 1, "Solar-Electric", 75, 50),
    (_EMAILS[2], 2, "Wind", 50, 75),
    (_EMAILS[2], 3, "Solar-Electric", 100, None),
    (_EMAILS[3], 1, "Solar-Electric", 100, None),
    (_EMAILS[3], 2, "Solar-Electric", 100, 75),
    (_EMAILS[3], 3, "Solar-Electric", 100, 250),
    (_EMAILS[4], 1, "Wind", 100, None),
    (_EMAILS[4], 2, "Wind", 100, None),
    (_EMAILS[5], 1, "Solar-Electric", 100, None),
]

# Name
MANUFACTURER = [
    ("Man1",),
    ("Man2",),
    ("Man3",),
    ("Man4",),
    ("Man5",),
    ("Man6",),
    ("Man7",),
    ("Man8",),
    ("Man9",),
    ("Man10",),
    ("Man11",),
    ("Man12",),
    ("Man13",),
    ("Man14",),
    ("Man15",),
    ("Man16",),
    ("Man17",),
    ("Man18",),
    ("Man19",),
    ("Man20",),
    ("Man21",),
    ("Man22",),
    ("Man23",),
    ("Man24",),
    ("Man25",),
    ("Man26",),
    ("Man27",),
    ("Man28",),
    ("Ban29",),
    ("Zan30",),
]
