from dataclasses import dataclass
import pathlib

import pandas as pd
import numpy as np

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()

POSTAL_CODES_FILE = "postal_codes.csv"
HOUSEHOLD_SEED_DATA_FILE = "Household.tsv"
APPLIANCE_SEED_DATA_FILE = "Appliance.tsv"
POWER_SEED_DATA_FILE = "Power.tsv"
MANUFACTURER_SEED_DATA_FILE = "Manufacturer.tsv"


@dataclass
class SeedData:
    household_seed: pd.DataFrame = None
    appliance_seed: pd.DataFrame = None
    power_generators_seed: pd.DataFrame = None
    manufacturer_seed: pd.DataFrame = None

    def __post_init__(self):
        self.load_household()
        self.load_appliance()
        self.load_power_generators()
        self.load_manufacturer()

    @staticmethod
    def _as_list_of_tuples(df: pd.DataFrame):
        """Transforms row values from a dataframe into a list of tuples for
        each row.
        """
        return [tuple(row) for row in df.values]

    def locations(self):
        """Imports postal code data from a csv."""

        # Define the column names and types
        columns = {
            "zip": str,
            "city": str,
            "state": str,
            "lat": float,
            "lon": float,
        }

        # Read the CSV file and apply the specified column names and types
        df = pd.read_csv(
            f"{CURRENT_DIR}/data/{POSTAL_CODES_FILE}",
            names=columns.keys(),
            skiprows=1,
            dtype=columns,
        )

        # Reorder the columns
        df = df.reindex(columns=["zip", "lon", "lat", "state", "city"])

        return self._as_list_of_tuples(df)

    def load_household(self):
        """Import data from a local tsv file."""

        # Read the CSV file and apply the specified column names and types
        columns = {
            "email": str,
            "household_type": str,
            "footage": int,
            "heating_temp": float,
            "cooling_temp": float,
            "postal_code": str,
            "utilities": str,
        }

        df = pd.read_csv(
            f"{CURRENT_DIR}/data/{HOUSEHOLD_SEED_DATA_FILE}",
            names=columns.keys(),
            skiprows=1,
            dtype=columns,
            sep="\t",
        )
        # sql inserts require None not nan
        df = df.replace({np.nan: None})

        self.household_seed = df

    def load_appliance(self):
        """Import data from a local tsv file."""

        # Read the CSV file and apply the specified column names and types
        # Two columns have the name energy source in the file so give unique names
        column_names = [
            "household_email",
            "appliance_number",
            "manufacturer_name",
            "model",
            "appliance_type",
            "air_handler_types",
            "eer",
            "heater_energy_source",
            "hspf",
            "seer",
            "water_heater_energy_source",
            "capacity",
            "temperature",
            "btu",
        ]
        df = pd.read_csv(
            f"{CURRENT_DIR}/data/{APPLIANCE_SEED_DATA_FILE}",
            sep="\t",
            header=0,
            names=column_names,
        )
        # sql inserts require None not nan
        df = df.replace({np.nan: None})

        self.appliance_seed = df

    def load_power_generators(self):
        """Import data from a local tsv file."""

        # Read the CSV file and apply the specified column names and types
        df = pd.read_csv(
            f"{CURRENT_DIR}/data/{POWER_SEED_DATA_FILE}",
            sep="\t",
        )
        # sql inserts require None not nan
        df = df.replace({np.nan: None})

        self.power_generators_seed = df

    def load_manufacturer(self):
        """Import data from a local tsv file."""

        # Read the CSV file and apply the specified column names and types
        df = pd.read_csv(
            f"{CURRENT_DIR}/data/{MANUFACTURER_SEED_DATA_FILE}",
            sep="\t",
        )
        # sql inserts require None not nan
        df = df.replace({np.nan: None})

        self.manufacturer_seed = df

    def households(self):
        df = self.household_seed
        # A household is on_grid if it has utilities
        df["on_grid"] = df["utilities"].notnull()
        df = df[
            [
                "email",
                "postal_code",
                "household_type",
                "on_grid",
                "footage",
                "heating_temp",
                "cooling_temp",
            ]
        ]
        return self._as_list_of_tuples(df)

    def household_utilities(self):
        df = self.household_seed
        # Only return households with utilities
        mask = df["utilities"].notna()
        df = df[mask]
        # If multiple utilities, break them up and create new rows
        df = df.assign(utilities=df["utilities"].str.split(",")).explode("utilities")
        df = df[
            [
                "email",
                "utilities",
            ]
        ]
        return self._as_list_of_tuples(df)

    def appliances(self):
        df = self.appliance_seed
        df = df[
            [
                "household_email",
                "appliance_number",
                "manufacturer_name",
                "appliance_type",
                "model",
                "btu",
            ]
        ]
        return self._as_list_of_tuples(df)

    def water_heaters(self):
        df = self.appliance_seed
        # Only get specific rows based on the air handler type
        mask = df["appliance_type"].notna() & (
            df["appliance_type"].str.contains("Water Heater")
        )
        df = df[mask]
        df = df[
            [
                "household_email",
                "appliance_number",
                "water_heater_energy_source",
                "temperature",
                "capacity",
            ]
        ]
        return self._as_list_of_tuples(df)

    def heat_pumps(self):
        df = self.appliance_seed
        # Only get specific rows based on the air handler type
        mask = df["air_handler_types"].notna() & (
            df["air_handler_types"].str.contains("heatpump")
        )
        df = df[mask]
        df = df[
            [
                "household_email",
                "appliance_number",
                "hspf",
                "seer",
            ]
        ]
        return self._as_list_of_tuples(df)

    def air_conditioners(self):
        df = self.appliance_seed
        # Only get specific rows based on the air handler type
        mask = df["air_handler_types"].notna() & (
            df["air_handler_types"].str.contains("air_conditioner")
        )
        df = df[mask]
        df = df[
            [
                "household_email",
                "appliance_number",
                "eer",
            ]
        ]
        return self._as_list_of_tuples(df)

    def heaters(self):
        df = self.appliance_seed
        # Only get specific rows based on the air handler type
        mask = df["air_handler_types"].notna() & (
            df["air_handler_types"].str.contains("heater")
        )
        df = df[mask]
        df = df[
            [
                "household_email",
                "appliance_number",
                "heater_energy_source",
            ]
        ]
        return self._as_list_of_tuples(df)

    def power_generators(self):
        df = self.power_generators_seed
        df = df[
            [
                "household_email",
                "power_number",
                "energy_source",
                "kilowatt_hours",
                "battery",
            ]
        ]
        return self._as_list_of_tuples(df)

    def manufacturers(self):
        return self._as_list_of_tuples(self.manufacturer_seed)


seed_data = SeedData()

LOCATION_DATA = seed_data.locations()
HOUSEHOLD_DATA = seed_data.households()
HOUSEHOLD_UTILITIES = seed_data.household_utilities()
APPLIANCE = seed_data.appliances()
WATER_HEATER = seed_data.water_heaters()
HEAT_PUMP = seed_data.heat_pumps()
AIR_CONDITIONER = seed_data.air_conditioners()
HEATER = seed_data.heaters()
POWER_GENERATOR = seed_data.power_generators()
MANUFACTURER = seed_data.manufacturers()
