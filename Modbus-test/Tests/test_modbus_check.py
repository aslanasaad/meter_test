#
# tests/test_modbus_check.py

import pytest
from pymodbus.exceptions import ModbusException
from src.ModbusTest import read_modbus_registers
import configparser

# Read from the .ini file
config = configparser.ConfigParser()
config.read('modbus_config.ini')

# Extract parameters from the .ini file
TEST_IP = config['Modbus']['ip_address']
TEST_PORT = int(config['Modbus']['port'])
START_ADDRESS = int(config['Modbus']['start_address'])
REGISTER_COUNT = int(config['Modbus']['register_count'])
SLAVE_ID = int(config['Modbus']['slave_id'])
EXPECTED_VALUE = int(config['Modbus']['expected_value'])

print("The value for the register modbus " + str(read_modbus_registers(TEST_IP, TEST_PORT, START_ADDRESS, REGISTER_COUNT, SLAVE_ID)))

# Define the test
def test_read_modbus_registers_success():
    try:
        values = read_modbus_registers(TEST_IP, TEST_PORT, START_ADDRESS, REGISTER_COUNT, SLAVE_ID)
        assert values[4] >= EXPECTED_VALUE
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
