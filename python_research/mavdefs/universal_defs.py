import dronekit
import time
from pymavlink.dialects.v10.python2 import ardupilotmega as mavlink

def get_vehicle(connection_string=None):
    """
    Connect to a vehicle listening on the given ip and port.

    :param connection_string: the string to connect to, in form 'tcp:IP:PORT' (see try statement for example)
    :return: the vehicle
    """
    try:
        if not connection_string:
            connection_string = 'tcp:127.0.0.1:5760' # Default connection string
        print("Connecting to vehicle on %s" % connection_string)
        vehicle = dronekit.connect(connection_string, wait_ready=True)
        print("Vehicle connected with ID %s" % vehicle._master.source_system)
        return vehicle
    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)

def measure_round_trip(vehicle, msg=None, listener_type=None):
    """
    Measures the round-trip transmission time of any given message from message_factory
    For a list of messages, see https://mavlink.io/en/messages/common.html and https://mavlink.io/en/messages/minimal.html

    :param vehicle: the vehicle to send the message to
    :param msg: the message_factory message
    :param listener_type: the type of message
    :return: the round-trip time
    """
    if not vehicle:
        raise ValueError("Vehicle object is None.")
    
    if msg is None or listener_type is None: # Set a default heartbeat message if None
        print("msg or listener_type is None, setting to default of heartbeat")
        msg = vehicle.message_factory.heartbeat_encode(
            mavlink.MAV_TYPE_GCS,
            mavlink.MAV_AUTOPILOT_INVALID,
            0,
            0,
            mavlink.MAV_STATE_ACTIVE
        )
        listener_type = 'HEARTBEAT'

    # Define a dictionary to capture the arm response time
    message_state = {'received': False}

    # Define callback function
    def callback(self, name, message):
        if not message_state['received']:
            print("Received %s message" % name)
            message_state['received'] = True

    # Add message listener
    vehicle.add_message_listener(listener_type, callback)
    print("Added listener for %s" % listener_type)

    # Record start time
    start_time = time.time()

    # Send message
    vehicle.send_mavlink(msg)
    print("Sent message")

    # Wait for response
    timeout = 5  # seconds
    while not message_state['received'] and (time.time() - start_time) < timeout:
        time.sleep(0.1)  # Sleep for a short period to avoid busy waiting

    if not message_state['received']:
        raise Exception("Did not receive a response within the timeout period.")
    
    # Record end time
    end_time = time.time()

    # Remove message listener
    vehicle.remove_message_listener(listener_type, callback)

    # Calculate round trip time
    round_trip_time = end_time - start_time
    return round_trip_time