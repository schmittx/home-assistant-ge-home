"""GE Kitchen Switch Entities"""
import async_timeout
import logging
from typing import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .entities import GeErdSwitch
from .const import DOMAIN
from .update_coordinator import GeKitchenUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: Callable):
    """GE Kitchen sensors."""
    _LOGGER.debug('Adding GE Kitchen switches')
    coordinator: GeKitchenUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # This should be a NOP, but let's be safe
    with async_timeout.timeout(20):
        await coordinator.initialization_future
    _LOGGER.debug('Coordinator init future finished')

    apis = list(coordinator.appliance_apis.values())
    _LOGGER.debug(f'Found {len(apis):d} appliance APIs')
    entities = [
        entity
        for api in apis
        for entity in api.entities
        if isinstance(entity, GeErdSwitch) and entity.erd_code in api.appliance._property_cache
    ]
    _LOGGER.debug(f'Found {len(entities):d} switches')
    async_add_entities(entities)
