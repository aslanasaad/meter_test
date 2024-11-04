# src/modbus_check.py

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException, ModbusException

def read_modbus_registers(ip, port, start_address, register_count, slave_id, timeout=10, retries=3):
    client = ModbusTcpClient(ip, port=port, timeout=timeout, retries=retries)
    connection = client.connect()
    if not connection:
        raise ConnectionError("Failed to connect to Modbus server")

    try:
        # Read the holding registers
        result = client.read_holding_registers(address=start_address, count=register_count, unit=slave_id)
        if result.isError():
            raise ModbusException(f"Error reading registers: {result}")

        # Write the Modbus values to a file
        output_file_path = "modbus_output.txt"
        with open(output_file_path, "w") as f:
            f.write(f"Modbus values: {result.registers}\n")

        # Print the location of the output file
        print(f"Output saved to: {output_file_path}")

        return result.registers

    except (ModbusIOException, ModbusException) as e:
        raise ModbusException(f"Modbus error: {e}")
    except Exception as e:
        raise e
    finally:
        client.close()

# Prompt to keep the console window open
input("Press Enter to close...")
