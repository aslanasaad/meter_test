import time
import matplotlib.pyplot as plt
from pydnp3 import opendnp3, openpal, asiopal, asiodnp3

# Configuration
outstation_ip = '192.168.0.167'
outstation_port = 20000  # Typical DNP3 port
polling_interval = 100  # in milliseconds
polling_duration = 10  # in seconds

# Initialize DNP3 manager
manager = asiodnp3.DNP3Manager(1)
manager.AddTCPClient("client", opendnp3.levels.NORMAL, asiopal.ChannelRetry.Default(), outstation_ip, outstation_port,
                     "0.0.0.0", 50000)


# Define a listener class to handle events
class MyListener(opendnp3.ISOEHandler):
    def __init__(self):
        self.response_times = []

    def Process(self, info, values):
        end_time = time.time()
        response_time = (end_time - self.start_time) * 1000  # Convert to milliseconds
        self.response_times.append(response_time)
        print(f"Response time: {response_time} ms")


listener = MyListener()


# Define an application class
class MyApplication(opendnp3.IMasterApplication):
    def OnReceiveIIN(self, iin):
        pass

    def OnTaskComplete(self, info):
        pass


application = MyApplication()

# Create master
stack = manager.AddMaster(
    "master",
    asiodnp3.PrintingChannelListener().Create(),
    asiodnp3.DefaultMasterApplication().Create(),
    listener,
    opendnp3.MasterStackConfig()
)


# Function to poll data
def poll_data():
    listener.start_time = time.time()
    request = opendnp3.ReadRequest()
    request.AddAllObjectsHeader(opendnp3.GroupVariationID(30, 2))  # Group 30, Variation 2 is Analog Inputs
    stack.AddReadTask(request)


# Polling loop
start_time = time.time()
while time.time() - start_time < polling_duration:
    poll_data()
    time.sleep(polling_interval / 1000.0)

manager.Shutdown()

# Data Analysis and Visualization
plt.plot(listener.response_times, label=f'Polling Interval {polling_interval} ms')
plt.xlabel('Polling Count')
plt.ylabel('Response Time (ms)')
plt.legend()
plt.title('DNP3 Response Times')
plt.show()
