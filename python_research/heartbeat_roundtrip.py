from mavdefs import universal_defs
import time
from pymavlink.dialects.v10.python2 import ardupilotmega as mavlink

def measure_heartbeat_roundtrip(vehicle):
    if not vehicle:
        raise ValueError("Vehicle object is None.")
    
    # Define a callback function to capture the heartbeat response time
    state = {'heartbeat_received': False}
    heartbeat_received = False
    def heartbeat_callback(message, *args):
        state['heartbeat_received'] = True

    vehicle.add_message_listener('HEARTBEAT', heartbeat_callback)

    start_time = time.time()

    # Send a heartbeat message using vehicle.message_factory
    heartbeat_msg = vehicle.message_factory.heartbeat_encode(
        type=mavlink.MAV_TYPE_GCS,
        autopilot=mavlink.MAV_AUTOPILOT_INVALID,
        base_mode=0,
        custom_mode=0,
        system_status=mavlink.MAV_STATE_ACTIVE
    )
    vehicle.send_mavlink(heartbeat_msg)

    # Wait for the heartbeat response
    timeout = 5  # seconds
    while not state['heartbeat_received'] and (time.time() - start_time) < timeout:
        time.sleep(0.1)  # Sleep for a short period to avoid busy waiting

    if not state['heartbeat_received']:
        raise TimeoutError("Did not receive a heartbeat response within the timeout period.")

    # Record the end time
    end_time = time.time()

    # Remove the listener
    vehicle.remove_message_listener('HEARTBEAT', heartbeat_callback)

    # Calculate the round-trip time
    round_trip_time = end_time - start_time
    return round_trip_time

connection_string = 'tcp:127.0.0.1:5760'
vehicle = universal_defs.get_vehicle(connection_string)

round_trip_time = measure_heartbeat_roundtrip(vehicle)

print("Round Trip Time: %s" % round_trip_time)