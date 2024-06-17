from dronekit import connect, VehicleMode, LocationGlobalRelative
from time import sleep

connection_string = 'tcp:127.0.0.1:5760' # Port and address mavlink
vehicle = connect(connection_string, wait_ready=True)

# Arms the vehicle (if armable)
def arm():
    if vehicle.is_armable:
        vehicle.armed = True
        print("Vehicle armed.")
    else:
        print("Unable to arm.")

# Disarms the vehicle
def disarm():
    vehicle.armed = False
    print("Vehicle disarmed.")

# Runs a simple takeoff to get to the takeoff altitude
def takeoff(target_altitude):
    if vehicle.armed:
        vehicle.simple_takeoff(target_altitude)
        print("Taking off...")
        while True: # Print altitude status while taking off
            print(" Altitude: %s" % vehicle.location.global_relative_frame.alt) # Print current altitude
            if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:  # Check if the vehicle is close to the target altitude
                print("Reached takeoff altitude.")
            break
        sleep(1)
    else:
        print("Cannot take off, vehicle is unarmed.")

# Move to a specific location
def goto(lat, lon, alt):
    target_location = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(target_location)

# Return to the launch point
def return_to_launch():
    vehicle.mode = VehicleMode("RTL")
    print("Returning to launch...")

# Land the drone
def land():
    vehicle.mode = VehicleMode("LAND")
    print("Landing...")

# Mission parameters
takeoff_altitude = 20
waypoints = [
    (38.21882, -85.7047507, takeoff_altitude),
    (38.21882, -85.7047607, takeoff_altitude),
    (38.21982, -85.7047607, takeoff_altitude),
]

# Takeoff
arm()
takeoff(takeoff_altitude)

# Visit waypoints
for lat, lon, alt in waypoints:
    goto(lat, lon, alt)
    sleep(5)

return_to_launch()

land()

vehicle.close()
print("Mission complete")