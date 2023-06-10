from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from db import queries
from db.inventory import (AirHandlerAC, AirHandlerHeater, AirHandlerHeatPump,
                          Appliance, WaterHeater)
from util import *

load_dotenv()

# Initialize Flask App

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Database


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, "psql_conn"):
        g.psql_conn.cursor().close()
        g.psql_conn.close()


# helper


def build_response(query_result):
    if query_result["status"] == "success":
        return jsonify({"status": 200, "data": query_result})
    else:
        return jsonify({"status": 400, "data": query_result})


def build_responses(query_results):
    for query_result in query_results:
        if query_result["status"] != "success":
            return jsonify({"status": 400, "data": query_result})
    return jsonify({"status": 200, "data": [q for q in query_results]})


# Household


@app.route("/api/household/create", methods=["POST"])
def api_household_create():
    email = request.json.get("email")
    postal_code = request.json.get("postalCode")
    type = request.json.get("type")
    square_footage = request.json.get("squareFootage")
    ts_heating = request.json.get("tsHeating")
    ts_cooling = request.json.get("tsCooling")
    on_grid = request.json.get("onGrid")

    household_query_result = queries.insert_household(
        email, postal_code, type, square_footage, ts_heating, ts_cooling, on_grid
    )

    if request.json.get("electric"):
        queries.insert_household_utility(email, "Electric")

    if request.json.get("gas"):
        queries.insert_household_utility(email, "Gas")

    if request.json.get("steam"):
        queries.insert_household_utility(email, "Steam")

    return build_response(household_query_result)


@app.route("/api/validations/email")
def api_validations_email():
    query_result = queries.validate_email(request.args.get("email").lower())

    if int(query_result["data"][0][0]) > 0:
        query_result["data"] = {"valid": False}
    else:
        query_result["data"] = {"valid": True}

    return build_response(query_result)


@app.route("/api/validations/postal-code")
def api_validations_postal_code():
    query_result = queries.validate_postal_code(request.args.get("postalCode"))

    if int(query_result["data"][0][0]) > 0:
        query_result["data"] = {"valid": True}
    else:
        query_result["data"] = {"valid": False}

    return build_response(query_result)


# Appliance


@app.route("/api/appliances")
def api_appliance_index():
    query_result = queries.appliance_index(request.json["email"])

    return build_response(query_result)


@app.route("/api/appliances/<string:email>")
def api_appliances(email):
    query_result = queries.appliance_index(email)

    return build_response(query_result)


@app.route("/api/appliances/create", methods=["POST"])
def api_appliance_create():
    """Insert based on appliance type.

    The response will have the following key:value pairs: {
        'appliance_number': 6,
        'email': test@gmail.com,
        'type': 'Air Handler',
        'manufacturer': 'Man2',
        'btu_rating': 5,
        'model': 'x', # optional
        'air_handler_heating_cooling_methods': {'AC': True, 'Heater': False, 'Heatpump': True},
        'air_handler_ac_eer': 5,
        'air_handler_heater_energy_source': 'Electric',
        'air_handler_heatpump_hspf': 5,
        'air_handler_heatpump_seer': 7,
        'water_heater_energy_source': '', # notice empty when appliance type not selected
        'water_heater_temperature': '',
        'water_heater_capacity': ''
    }
    """
    # Common
    email = request.json.get("email")
    appliance_number = request.json.get("appliance_number")
    appliance = Appliance(
        email,
        appliance_number,
        request.json.get("manufacturer"),
        request.json.get("type"),
        request.json.get("model"),  # None represented as empty string
        request.json.get("btu_rating"),
    )
    # Air Handler
    air_handler_ac = AirHandlerAC(
        email,
        appliance_number,
        request.json.get("air_handler_ac_eer"),
    )
    air_handler_heater = AirHandlerHeater(
        email,
        appliance_number,
        request.json.get("air_handler_heater_energy_source"),
    )
    air_handler_heat_pump = AirHandlerHeatPump(
        email,
        appliance_number,
        request.json.get("air_handler_heatpump_hspf"),
        request.json.get("air_handler_heatpump_seer"),
    )
    # Water Heater
    water_heater = WaterHeater(
        email,
        appliance_number,
        request.json.get("water_heater_energy_source"),
        request.json.get("water_heater_temperature") or None,  # Optional
        request.json.get("water_heater_capacity"),
    )
    if appliance.type == "Air Handler":
        appliance_result = queries.insert_appliance(appliance)
        results = [appliance_result]
        heat_cool_options = request.json.get("air_handler_heating_cooling_methods")
        if heat_cool_options.get("AC"):
            ac_result = queries.insert_air_handler_air_conditioner(air_handler_ac)
            results.append(ac_result)
        if heat_cool_options.get("Heater"):
            heater_result = queries.insert_air_handler_heater(air_handler_heater)
            results.append(heater_result)
        if heat_cool_options.get("Heatpump"):
            heat_pump_result = queries.insert_air_handler_heat_pump(
                air_handler_heat_pump
            )
            results.append(heat_pump_result)
        return build_responses(results)

    elif appliance.type == "Water Heater":
        appliance_result = queries.insert_appliance(appliance)
        water_heater_result = queries.insert_water_heater(water_heater)
        results = [appliance_result, water_heater_result]
        return build_responses(results)


@app.route(
    "/api/appliance-delete/<string:appliance_id>/<string:email>", methods=["DELETE"]
)
def api_appliance_delete(appliance_id, email):
    query_result = queries.appliance_delete(
        email,
        appliance_id,
    )

    return build_response(query_result)


# Power Generation


@app.route("/api/power-generation")
def api_power_generation_index():
    query_result = queries.power_generation_index(request.json["email"])

    return build_response(query_result)


@app.route("/api/power-generation/create", methods=["POST"])
def api_power_generation_create():
    email = request.json.get("email")
    type = request.json.get("type")
    monthlyKWh = request.json.get("monthlyKWh")
    storageKWh = request.json.get("storageKWh")

    pgNum = request.json.get("pgNum")
    email = request.json.get("email")
    type = request.json.get("type")
    monthlyKWh = request.json.get("monthlyKWh")
    storageKWh = request.json.get("storageKWh")

    query_result = queries.insert_power_generation(
        pgNum, email, type, monthlyKWh, storageKWh
    )

    return build_response(query_result)


@app.route("/api/power-generation-methods-list/<string:email>", methods=["GET"])
def api_power_generation_methods(email):
    query_result = queries.power_generation_methods(
        email,
    )

    return build_response(query_result)


@app.route(
    "/api/power-generation-delete/<string:power_generation_id>/<string:email>",
    methods=["DELETE"],
)
def api_power_generation_delete(power_generation_id, email):
    query_result = queries.power_generation_methods_delete(
        email,
        power_generation_id,
    )

    return build_response(query_result)


# Manufacturer


@app.route("/api/manufacturers-names")
def api_reports_manufacturers_names():
    query_result = queries.manufacturer_names()
    print(query_result)

    return build_response(query_result)


# Manufacturer reports


@app.route("/api/reports/manufacturers")
def api_reports_manufacturers():
    query_result = queries.manufacturer_index()

    return build_response(query_result)


@app.route("/api/reports/manufacturer-drilldown/<name>")
def api_reports_manufacturer_detail(name):
    query_result = queries.manufacturer_detail(name)

    return build_response(query_result)


@app.route("/api/reports/model-search")
def api_reports_manufacturer_search_create():
    q = request.args.get("q").lower()
    if not valid_search_term(q):
        query_result = {"status": 400, "err": f"Invalid Search '{q}'"}
    else:
        query_result = queries.manufacturer_search(q)
        print("RESULT", query_result)

    return build_response(query_result)


# Heating/Cooling Method


@app.route("/api/reports/hcm")
def api_reports_hcm():
    query_result = queries.hcm_index()

    return build_response(query_result)


# Water Heater


@app.route("/api/reports/water-heaters")
def api_reports_water_heater():
    query_result = queries.water_heater_index()

    return build_response(query_result)


@app.route("/api/reports/water-heaters/<state>")
def api_reports_water_heater_state(state):
    query_result = queries.water_heater_detail(state)
    return build_response(query_result)


# Off Grid Dashboard


@app.route("/api/reports/off-grid")
def api_reports_off_grid():
    off_grid_results = {
        "data": {
            "state_records": queries.off_grid_state(),
            "pg_records": queries.off_grid_pg(),
            "pg_type_records": queries.off_grid_pg_types(),
            "average_records": queries.off_grid_averages(),
            "btu_records": queries.off_grid_btus(),
        },
        "status": 200,
    }
    return jsonify(off_grid_results)


# Radius


@app.route("/api/reports/radius")
def reports_radius_create():
    r = int(request.args.get("r"))
    zip = request.args.get("zip")

    if not valid_postal_code(zip):
        query_result = {"status": 400, "err": "Invalid Postal Code"}
    elif not valid_search_radius(r):
        query_result = {"status": 400, "err": "Invalid Search Radius"}
    else:
        query_result = queries.radius_detail(zip, r)

    return build_response(query_result)
