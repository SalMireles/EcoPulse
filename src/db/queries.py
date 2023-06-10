from util import get_db

from .query_strings import *
from db.inventory import (
    Appliance,
    AirHandlerAC,
    AirHandlerHeater,
    AirHandlerHeatPump,
    WaterHeater,
)


def db_decorator(func):
    def wrapper(*args, **kwargs):
        conn = get_db()
        cur = conn.cursor()

        try:
            func(cur, *args, **kwargs)
            if func.__name__ in [
                "insert_household",
                "insert_household_utility",
                "insert_power_generation",
                "insert_appliance",
                "insert_water_heater",
                "insert_air_handler_air_conditioner",
                "insert_air_handler_heater",
                "insert_air_handler_heat_pump",
            ]:
                return {"status": "success"}
            else:
                return {
                    "status": "success",
                    "headings": [i[0] for i in cur.description],
                    "data": [[str(x) for x in i] for i in cur.fetchall()],
                }
        except Exception as error:
            print(error)
            return {
                "status": "err",
                "err": "There was a problem processing your request.",
            }

    return wrapper


@db_decorator
def validate_email(cur, email):
    cur.execute(validate_email_sql, (email,))


@db_decorator
def validate_postal_code(cur, postal_code):
    cur.execute(validate_postal_code_sql, (postal_code,))


@db_decorator
def insert_household(
    cur,
    email,
    postal_code,
    type,
    square_footage,
    thermostat_setting_heating,
    thermostat_setting_cooling,
    on_grid,
):
    cur.execute(
        insert_household_sql,
        (
            email,
            postal_code,
            type.lower(),
            square_footage,
            thermostat_setting_heating,
            thermostat_setting_cooling,
            on_grid,
        ),
    )


@db_decorator
def insert_household_utility(cur, email, utility):
    cur.execute(insert_household_utility_sql, (email, utility))


@db_decorator
def insert_appliance(cur, appliance: Appliance):
    cur.execute(
        insert_appliance_sql,
        appliance.as_tuple(),
    )


@db_decorator
def insert_water_heater(cur, water_heater: WaterHeater):
    cur.execute(
        insert_water_heater_sql,
        water_heater.as_tuple(),
    )


@db_decorator
def insert_air_handler_air_conditioner(cur, ac: AirHandlerAC):
    cur.execute(
        insert_air_handler_air_conditioner_sql,
        ac.as_tuple(),
    )


@db_decorator
def insert_air_handler_heater(cur, heater: AirHandlerHeater):
    cur.execute(
        insert_air_handler_heater_sql,
        heater.as_tuple(),
    )


@db_decorator
def insert_air_handler_heat_pump(cur, heat_pump: AirHandlerHeatPump):
    cur.execute(
        insert_air_handler_heat_pump_sql,
        heat_pump.as_tuple(),
    )


@db_decorator
def insert_power_generation(cur, pgNum, email, type, monthlyKWh, storageKWh):
    cur.execute(
        insert_power_generation_sql, (pgNum, email, type, monthlyKWh, storageKWh)
    )


@db_decorator
def power_generation_methods(cur, email):
    cur.execute(power_generation_methods_sql, (email,))


@db_decorator
def power_generation_methods_delete(cur, email, power_generation_id):
    cur.execute(power_generation_methods_delete_sql, (email, power_generation_id))


@db_decorator
def appliance_delete(cur, email, appliance_id):
    cur.execute(appliance_delete_sql, (email, appliance_id))


@db_decorator
def appliance_index(cur, email):
    cur.execute(appliance_index_sql, (email,))


@db_decorator
def power_generation_index(cur, email):
    cur.execute(power_generation_index_sql, (email,))


@db_decorator
def manufacturer_names(cur):
    cur.execute(manufacturer_names_sql)


@db_decorator
def manufacturer_index(cur):
    cur.execute(manufacturer_index_sql)


@db_decorator
def manufacturer_detail(cur, name):
    cur.execute(manufacturer_detail_sql, (name,))


@db_decorator
def manufacturer_search(cur, term):
    cur.execute(manufacturer_search_sql, (term, term))


@db_decorator
def hcm_index(cur):
    cur.execute(hcm_index_sql)


@db_decorator
def water_heater_index(cur):
    cur.execute(water_heater_index_sql)


@db_decorator
def water_heater_detail(cur, term):
    cur.execute(water_heater_detail_sql, (term,))


@db_decorator
def off_grid_state(cur):
    cur.execute(off_grid_state_sql)


@db_decorator
def off_grid_pg(cur):
    cur.execute(off_grid_pq_sql)


@db_decorator
def off_grid_pg_types(cur):
    cur.execute(off_grid_pg_types_sql)


@db_decorator
def off_grid_averages(cur):
    cur.execute(off_grid_averages_sql)


@db_decorator
def off_grid_btus(cur):
    cur.execute(off_grid_btus_sql)


@db_decorator
def radius_detail(cur, postal_code, miles):
    cur.execute(radius_detail_sql, (postal_code, miles))
