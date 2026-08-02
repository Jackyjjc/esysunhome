"""Tests for ESY Sunhome sensor entities."""

from types import SimpleNamespace
from unittest.mock import Mock

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy

from custom_components.esy_sunhome.const import CONF_DEVICE_ID
from custom_components.esy_sunhome.sensor import (
    DailyBattChargeSensor,
    DailyBattDischargeSensor,
)


def test_daily_battery_charge_sensor_handles_daily_resets() -> None:
    """Daily battery charge is a resetting, monotonically increasing meter."""
    coordinator = SimpleNamespace(
        api=SimpleNamespace(device_id="device-id"),
        config_entry=SimpleNamespace(data={CONF_DEVICE_ID: "device-id"}),
        data={"dailyBattCharge": 22.68},
    )
    sensor = DailyBattChargeSensor(coordinator)
    sensor.async_write_ha_state = Mock()

    sensor._handle_coordinator_update()

    assert sensor.state_class is SensorStateClass.TOTAL_INCREASING
    assert sensor.device_class is SensorDeviceClass.ENERGY
    assert sensor.native_unit_of_measurement is UnitOfEnergy.KILO_WATT_HOUR
    assert sensor.native_value == 22.68
    assert sensor.unique_id == "device-id_dailyBattCharge"
    sensor.async_write_ha_state.assert_called_once_with()


def test_daily_battery_discharge_sensor_handles_daily_resets() -> None:
    """Daily battery discharge is a resetting, increasing meter."""
    coordinator = SimpleNamespace(
        api=SimpleNamespace(device_id="device-id"),
        config_entry=SimpleNamespace(data={CONF_DEVICE_ID: "device-id"}),
        data={"dailyBattDischarge": 4.27},
    )
    sensor = DailyBattDischargeSensor(coordinator)
    sensor.async_write_ha_state = Mock()

    sensor._handle_coordinator_update()

    assert sensor.state_class is SensorStateClass.TOTAL_INCREASING
    assert sensor.device_class is SensorDeviceClass.ENERGY
    assert sensor.native_unit_of_measurement is UnitOfEnergy.KILO_WATT_HOUR
    assert sensor.native_value == 4.27
    assert sensor.unique_id == "device-id_dailyBattDischarge"
    sensor.async_write_ha_state.assert_called_once_with()
