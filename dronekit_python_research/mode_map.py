from dronekit import connect

# Connect to the Vehicle (SITL)
connection_string = 'tcp:127.0.0.1:5760'  # Default SITL connection string
print("Connecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)

# Check if mode_mapping is available
if hasattr(vehicle._master, 'mode_mapping'):
    mode_mapping = vehicle._master.mode_mapping()
    print("Available flight modes and their IDs:")
    for mode, mode_id in mode_mapping.items():
        print("Mode: {}, ID: {}".format(mode, mode_id))
else:
    print("The vehicle does not have a mode_mapping attribute")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

print("Completed")
