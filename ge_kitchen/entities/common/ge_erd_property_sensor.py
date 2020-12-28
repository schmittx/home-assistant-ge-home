from typing import Optional

from gekitchen import ErdCode, ErdCodeType, ErdMeasurementUnits
from ge_kitchen.devices import ApplianceApi
from .ge_erd_sensor import GeErdSensor


class GeErdPropertySensor(GeErdSensor):
    """GE Entity for sensors"""
    def __init__(self, api: ApplianceApi, erd_code: ErdCodeType, erd_property: str):
        super().__init__(api, erd_code)
        self.erd_property = erd_property

    @property
    def unique_id(self) -> Optional[str]:
        return f"{super().unique_id}_{self.erd_property}"

    @property
    def name(self) -> Optional[str]:
        base_string = super().name
        property_name = self.erd_property.replace("_", " ").title()
        return f"{base_string} {property_name}"

    @property
    def state(self) -> Optional[str]:
        try:
            value = getattr(self.appliance.get_erd_value(self.erd_code), self.erd_property)
        except KeyError:
            return None
        return stringify_erd_value(self.erd_code, value, self.units)

    @property
    def measurement_system(self) -> Optional[ErdMeasurementUnits]:
        return self.appliance.get_erd_value(ErdCode.TEMPERATURE_UNIT)

    @property
    def units(self) -> Optional[str]:
        return get_erd_units(self.erd_code, self.measurement_system)

    @property
    def device_class(self) -> Optional[str]:
        if self.erd_code in TEMPERATURE_ERD_CODES:
            return "temperature"
        return None
