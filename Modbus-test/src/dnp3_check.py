# src/brew install boost.py

from pydnp3 import opendnp3, asiodnp3, asiopal


def read_dnp3_points(ip, port, start_address, point_count, timeout=10):
    manager = asiodnp3.DNP3Manager(1)
    channel = manager.AddTCPClient('client',
                                   asiopal.ChannelRetry.Default(),
                                   [ip],
                                   '0.0.0.0',
                                   port,
                                   asiodnp3.PrintingChannelListener().Create())

    master_application = asiodnp3.PrintingMasterApplication()
    stack_config = asiodnp3.DefaultMasterStackConfig()
    master = channel.AddMaster('master',
                               asiodnp3.PrintingSOEHandler().Create(),
                               master_application,
                               stack_config)

    master.AddStateListener(lambda state: print(f"State changed: {state}"))
    channel_log = asiopal.LogFilters(opendnp3.levels.NOTHING | opendnp3.levels.ERROR)
    master_log = asiopal.LogFilters(opendnp3.levels.NOTHING | opendnp3.levels.ERROR)

    master.Enable()

    # Define a function to read points
    def read_points():
        values = []

        def callback(result):
            for measurement in result.GetValues():
                values.append(measurement.value)

        master.ScanRange(opendnp3.GroupVariationID(30, 2), start_address, start_address + point_count - 1).Then(
            callback)
        return values

    import time
    start_time = time.time()
    while time.time() - start_time < timeout:
        points = read_points()
        if len(points) == point_count:
            break
        time.sleep(1)

    if len(points) != point_count:
        raise TimeoutError("Failed to read DNP3 points within the timeout period")

    manager.Shutdown()
    return points
