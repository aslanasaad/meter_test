# tests/test_dnp3_check.py

import pytest
from src.dnp3_check import read_dnp3_points

# Define test parameters
TEST_IP = '192.168.0.176'
TEST_PORT = 20000
START_ADDRESS = 0
POINT_COUNT = 2
EXPECTED_FIRST_VALUE = 0 # Replace with the actual expected first value
MINIMUM_SECOND_VALUE = 220

def test_read_dnp3_points_success():
    try:
        values = read_dnp3_points(TEST_IP, TEST_PORT, START_ADDRESS, POINT_COUNT)
        assert values[0] == EXPECTED_FIRST_VALUE, f"Expected first value {EXPECTED_FIRST_VALUE}, but got {values[0]}"
        assert values[1] > MINIMUM_SECOND_VALUE, f"Expected second value to be greater than {MINIMUM_SECOND_VALUE}, but got {values[1]}"
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
