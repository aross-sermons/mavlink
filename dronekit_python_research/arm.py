from dronekit import connect, VehicleMode
from pymavlink.dialects.v10.python2 import ardupilotmega as mavlink
import time

# Connect to the Vehicle (SITL)
connection_string = 'tcp:127.0.0.1:5760'  # Default SITL connection string
print("Connecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)

# Define function to send MAVLink command to change flight mode
def set_mode():
    msg = vehicle.message_factory.set_mode_encode(
        0,  # target system
        mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,  # base mode
        4  # custom mode
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()

# Define function to arm the vehicle
def arm_vehicle():
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)
    
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)
    
    print("Vehicle is armed.")

# Change flight mode to GUIDED
print("Changing flight mode to GUIDED")
set_mode()
print("Vehicle Mode: %s" % vehicle.mode)

# Arm the vehicle
arm_vehicle()

print("Vehicle Mode: %s" % vehicle.mode)

# Ensure the script doesn't exit immediately
time.sleep(10)

print("Vehicle Mode: %s" % vehicle.mode)

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

print("Completed")
