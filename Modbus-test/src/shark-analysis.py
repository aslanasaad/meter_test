import pyshark

# Load the packet capture file
pcap_file = 'C:/Users/aslan.assad/OneDrive - NovaTech Process Solutions LLC/Desktop/aslan.pcapng'
capture = pyshark.FileCapture(pcap_file)

# Function to filter Modbus packets
def filter_modbus_packets(capture):
    modbus_packets = []
    for packet in capture:
        try:
            if 'modbus' in packet:
                modbus_packets.append(packet)
        except:
            continue
    return modbus_packets

# Extract Modbus packets
modbus_packets = filter_modbus_packets(capture)

# Show a summary of the Modbus packets
modbus_summary = []
for packet in modbus_packets:
    try:
        summary = {
            'timestamp': packet.sniff_time,
            'source': packet.ip.src,
            'destination': packet.ip.dst,
            'protocol': packet.transport_layer,  # Transport layer protocol
            'length': packet.length,  # Packet length
            'info': packet.highest_layer  # Highest layer protocol
        }
        modbus_summary.append(summary)
    except AttributeError as e:
        print(f"Attribute error: {e}")

# Display first 5 Modbus packets for summary
for summary in modbus_summary[:5]:
    print(summary)
