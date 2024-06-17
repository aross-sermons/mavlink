import dronekit
import time

# Connect to vehicle using default or given connection string
def get_vehicle(connection_string=None):
    try:
        if not connection_string:
            connection_string = 'tcp:127.0.0.1:5760' # Default connection string
        print("Connecting to vehicle on %s" % connection_string)
        vehicle = dronekit.connect(connection_string, wait_ready=True)
        return vehicle
    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
