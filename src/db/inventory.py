from dataclasses import asdict, dataclass


# Appliances
@dataclass
class BaseAppliance:
    email: str
    appliance_number: int

    def as_tuple(self):
        """Returns class attribute values in the order defined."""
        return tuple(asdict(self).values())


@dataclass
class Appliance(BaseAppliance):
    manufacturer_name: str
    type: str
    model_name: str
    btu_rating: int


@dataclass
class AirHandlerAC(BaseAppliance):
    air_ac_eer: float


@dataclass
class AirHandlerHeater(BaseAppliance):
    air_heater_energy_source: str


@dataclass
class AirHandlerHeatPump(BaseAppliance):
    air_heatpump_hspf: float
    air_heatpump_seer: float


@dataclass
class WaterHeater(BaseAppliance):
    water_heater_energy_source: str
    temperature: int
    capacity: float
