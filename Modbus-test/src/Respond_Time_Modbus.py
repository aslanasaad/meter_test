import time
from pymodbus.client import ModbusTcpClient
import pandas as pd
import matplotlib.pyplot as plt


# Configuration
meter_ip = '192.168.0.176'
register_count = 40
polling_interval = 100  # in milliseconds
polling_duration = 10  # in seconds

# Initialize Modbus client
client = ModbusTcpClient(meter_ip)

# Check if client connection is successful
if not client.connect():
    print(f"Failed to connect to Modbus server at {meter_ip}")
else:
    # Data collection
    response_times = []
    instance_counts = []
    interval_times = []
    successful_polls = 0
    failed_polls = 0
    read_durations = []
    successful_reads = []
    registers_read = []
    all_registers_values = []

    # Function to poll data
    def poll_data(client, count, last_poll_time, successful_polls, failed_polls):
        start_time = time.time()
        response = client.read_holding_registers(0, register_count)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds

        if response.isError():
            print(f"Poll {count}: Error reading registers")
            failed_polls += 1
        else:
            response_times.append(response_time)
            instance_counts.append(count)
            interval_time = (start_time - last_poll_time) * 1000  # Convert to milliseconds
            interval_times.append(interval_time)
            successful_polls += 1

            # Calculate the read duration
            read_duration = (end_time - start_time) * 1000  # Convert to milliseconds
            read_durations.append(read_duration)
            successful_reads.append(count)

            # Check how many registers were read
            num_registers = len(response.registers)
            registers_read.append(num_registers)

            # Save the values of each register
            all_registers_values.append(response.registers)

            # Print the values of each register
            print(f"Poll {count}: Successfully read {num_registers} registers")
            for i, value in enumerate(response.registers):
                print(f"Register {i + 1}: {value}")

        return end_time, successful_polls, failed_polls


    # Polling loop
    count = 1
    start_time = time.time()
    last_poll_time = start_time
    while time.time() - start_time < polling_duration:
        last_poll_time, successful_polls, failed_polls = poll_data(client, count, last_poll_time, successful_polls,
                                                                   failed_polls)
        count += 1
        time.sleep(polling_interval / 1000.0)

    client.close()

    # Save data to DataFrame and then to Excel file
    df = pd.DataFrame(all_registers_values, columns=[f'Register {i+1}' for i in range(register_count)])
    df.index.name = 'Poll Number'
    df.to_excel('register_values.xlsx')

    # Calculate average response time
    if response_times:
        average_response_time = sum(response_times) / len(response_times)
        print(f"Average Response Time: {average_response_time:.2f} ms")

    # Data Analysis and Visualization
    plt.figure(figsize=(10, 16))

    # Plot response times
    plt.subplot(4, 1, 1)
    plt.plot(instance_counts, response_times, label='Response Time')
    plt.scatter(successful_reads,
                [response_times[i] for i in range(len(response_times)) if instance_counts[i] in successful_reads],
                color='green', marker='o', label='Successful Reads')
    plt.axhline(y=average_response_time, color='r', linestyle='--')
    plt.text(len(instance_counts) / 2, average_response_time, f'Average: {average_response_time:.2f} ms', color='red',
             ha='center')
    plt.xlabel('Number of Instances')
    plt.ylabel('Response Time (ms)')
    plt.legend()
    plt.title('Modbus Poll/Response Performance')
    plt.grid(True)

    # Plot interval times
    plt.subplot(4, 1, 2)
    plt.plot(instance_counts, interval_times, label='Interval Time', color='orange')
    plt.scatter(successful_reads,
                [interval_times[i] for i in range(len(interval_times)) if instance_counts[i] in successful_reads],
                color='green', marker='o', label='Successful Reads')
    plt.xlabel('Number of Instances')
    plt.ylabel('Interval Time (ms)')
    plt.legend()
    plt.title('Polling Interval Times')
    plt.grid(True)

    # Plot read durations
    plt.subplot(4, 1, 3)
    plt.plot(instance_counts, read_durations, label='Read Duration', color='green')
    plt.scatter(successful_reads,
                [read_durations[i] for i in range(len(read_durations)) if instance_counts[i] in successful_reads],
                color='red', marker='o', label='Successful Reads')
    plt.xlabel('Number of Instances')
    plt.ylabel('Read Duration (ms)')
    plt.legend()
    plt.title('Read Duration Times')
    plt.grid(True)

    # Plot number of registers read
    plt.subplot(4, 1, 4)
    plt.plot(successful_reads, registers_read, label='Registers Read', color='blue')
    plt.scatter(successful_reads, registers_read, color='purple', marker='o', label='Successful Reads')
    plt.xlabel('Number of Instances')
    plt.ylabel('Registers Read')
    plt.legend()
    plt.title('Number of Registers Read')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Print summary of polling results
    print(f"Successful Polls: {successful_polls}")
    print(f"Failed Polls: {failed_polls}")
    print(f"Read Durations: {read_durations}")
    print(f"Registers Read: {registers_read}")
