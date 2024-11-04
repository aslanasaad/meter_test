# tests/test_modbus_check.py

import pytest
from pymodbus.exceptions import ModbusException
from src.ModbusTest import read_modbus_registers


# Define test parameters
TEST_IP = '192.168.0.176'
TEST_PORT = 502
START_ADDRESS = 0
REGISTER_COUNT = 5
SLAVE_ID = 0
EXPECTED_VALUE = 26500 # Replace with the actual expected first value
print("The value for the register modbus " + str(read_modbus_registers(TEST_IP, TEST_PORT, START_ADDRESS, REGISTER_COUNT, SLAVE_ID)))

def test_read_modbus_registers_success():
    try:
        values = read_modbus_registers(TEST_IP, TEST_PORT, START_ADDRESS, REGISTER_COUNT, SLAVE_ID)
        assert values[4] >= EXPECTED_VALUE
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")