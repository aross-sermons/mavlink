import dronekit
from pymavlink.dialects.v10.python2 import ardupilotmega as mavlink
import time

def get_vehicle(connection_string='tcp:127.0.0.1:5760') -> dronekit.Vehicle:
    """
    Connect to a vehicle listening on the given ip and port.

    :param connection_string: the string to connect to, in form 'tcp:IP:PORT' (see try statement for example)
    :return: the vehicle
    """
    try:
        vehicle = dronekit.connect(connection_string, wait_ready=True)
        print("Vehicle connected with ID %s" % vehicle._master.source_system)
        return vehicle
    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def print_mode_mapping(vehicle:dronekit.Vehicle):
    """
    
    """
    try:
        if hasattr(vehicle._master, 'mode_mapping'):
            mode_mapping = vehicle._master.mode_mapping()
            print("Available flight modes and their IDs:")
            for mode, mode_id in mode_mapping.items():
                print("Mode: {}, ID: {}".format(mode, mode_id))
            return
        else:
            print("The vehicle does not have a mode_mapping attribute")
            return
    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def arm_message_factory(vehicle:dronekit.Vehicle):
    """
    
    """
    try:
        arm_msg = vehicle.message_factory.command_long_encode(
            vehicle._master.target_system, # target system
            vehicle._master.target_component, # target component
            mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
            0, # confirmation
            1, # arm (0-1)
            0, 0, 0, 0, 0, 0 # unused params
        )

        # Send message, flush forces command queue to empty
        vehicle.send_mavlink(arm_msg)
        vehicle.flush()

        # Wait for vehicle to arm
        while not vehicle.armed:
            print("Waiting for vehicle to arm...")
            time.sleep(1)

        print("vehicle.armed = %s" % vehicle.armed)

    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def disarm_message_factory(vehicle:dronekit.Vehicle):
    """
    
    """
    try:
        arm_msg = vehicle.message_factory.command_long_encode(
            vehicle._master.target_system, # target system
            vehicle._master.target_component, # target component
            mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
            0, # confirmation
            0, # arm (0-1)
            0, 0, 0, 0, 0, 0 # unused params
        )

        # Send message, flush forces command queue to empty
        vehicle.send_mavlink(arm_msg)
        vehicle.flush()

        # Wait for vehicle to disarm
        while vehicle.armed:
            print("Waiting for vehicle to disarm...")
            time.sleep(1)

        print("vehicle.armed = %s" % vehicle.armed)

    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def set_mode_message_factory(vehicle:dronekit.Vehicle, mode='STABILIZE'):
    """
    
    """
    try:
        set_mode_msg = vehicle.message_factory.set_mode_encode(
            vehicle._master.target_system,  # target system
            mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,  # base mode
            vehicle._master.mode_mapping()[mode]  # custom mode
        )

        # Send message, flush forces command queue to empty
        vehicle.send_mavlink(set_mode_msg)
        vehicle.flush()

        # Wait for mode to change
        while not vehicle.mode.name == mode:
            print("Waiting for mode change...")
            time.sleep(1)

        print("vehicle.mode.name =  %s" % vehicle.mode.name)

    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def takeoff_message_factory(vehicle:dronekit.Vehicle, target_altitude:int):
    """
    
    """
    try:
        takeoff_msg = vehicle.message_factory.command_long_encode(
        vehicle._master.target_system, # target system
        vehicle._master.target_component, # target component
        mavlink.MAV_CMD_NAV_TAKEOFF, # command
        0, # confirmation
        0, # param1: Minimum pitch (if airspeed sensor present), in degrees
        0, 0, # param2-3: Empty parameters
        0, # param4: Yaw angle (if zero, the current yaw heading is used)
        float('nan'), # param5: Latitude
        float('nan'), # param6: Longitude
        target_altitude  # param7: Altitude
        )

        # Send message, flush forces command queue to empty
        vehicle.send_mavlink(takeoff_msg)
        vehicle.flush()

        # Wait for vehicle to reach target altitude
        while vehicle.location.global_relative_frame.alt < target_altitude * 0.95:
            print("Altitude: %s" % vehicle.location.global_relative_frame.alt)
            time.sleep(1)

        print("Target altitude reached: %s" %vehicle.location.global_relative_frame.alt)
    
    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def land_message_factory(vehicle:dronekit.Vehicle):
    """
    
    """
    try:
        land_msg = vehicle.message_factory.command_long_encode(
            vehicle._master.target_system, # target system
            vehicle._master.target_component, # target component
            mavlink.MAV_CMD_NAV_LAND,  # command
            0,       # confirmation
            0,
            0, 0, 0, 0, 0, 0
        )

        # Send message, flush forces command queue to empty
        vehicle.send_mavlink(land_msg)
        vehicle.flush()

        # Wait for vehicle to land (disarms automatically)
        while vehicle.armed:
            print("Altitude: %s" % vehicle.location.global_relative_frame.alt)
            time.sleep(1)

        print("Vehicle landed at altitude: %s" %vehicle.location.global_relative_frame.alt)
        print("vehicle.armed = %s" % vehicle.armed)

    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def move_velocity_message_factory(vehicle:dronekit.Vehicle, velocity_x:int, velocity_y:int, duration:int=None):
    """
    
    """
    try:
        if duration == None: # For safety, don't move if a duration isn't provided
            print("No duration for move_velocity_message_factory command. Please provide a duration.")
            return
        move_velocity_msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0, # time_boot_ms (not used)
            vehicle._master.target_system, # target system
            vehicle._master.target_component, # target component
            mavlink.MAV_FRAME_LOCAL_NED, # frame
            0b0000111111000111, # type_mask (only velocities enabled)
            0, 0, 0, # x, y, z positions (not used)
            velocity_x, velocity_y, 0, # x, y, z velocity in m/s
            0, 0, 0, # x, y, z acceleration (not used)
            0, 0) # yaw, yaw_rate (not used)
        
        # Send message, flush forces command queue to empty
        vehicle.send_mavlink(move_velocity_msg)
        vehicle.flush()

        # Repeat move command until duration is reached
        for _ in range(duration):
            vehicle.send_mavlink(move_velocity_msg)
            print("Vehicle Global Position (lat, lon, alt): %f, %f, %f" % (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon,vehicle.location.global_frame.alt))
            time.sleep(1)

        print("Vehicle finished moving")
        print("Vehicle Global Position (lat, lon, alt): %f, %f, %f" % (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon,vehicle.location.global_frame.alt))
        print("Vehicle Relative Altitude: %f" % vehicle.location.global_relative_frame.alt)
        print("Vehicle Relative Position (north, east, down): %f, %f, %f" % (vehicle.location.local_frame.north,vehicle.location.local_frame.east, vehicle.location.local_frame.down))

    except dronekit.APIException as e:
        print("Dronekit APIException: %s" % e)
    except Exception as e:
        print("Error: %s" % e)

def box_mission_velocity(vehicle:dronekit.Vehicle, velocity_x:int, velocity_y:int, velocity_duration:int, pause_duration:int):
    """
    Moves the drone in a box shape in the direction on velocity_x, then velociy_y, 
    then opposite velocity_x, then opposite velocity_y, for velocity_duration seconds.
    Pauses for pause_duration seconds between each movement.

    :param vehicle: The vehicle to send commands to.
    :param velocity_x: The velocity (speed and direction) to move the drone initially.
    :param velocity_y: The velocity (cpeed and direction) to move the drone initially.
    :param velocity_duration: The length of time each drone movement will take.
    :param pause_duration: The length of time between drone movements.
    """
    move_velocity_message_factory(vehicle, velocity_x, 0, velocity_duration)

    time.sleep(pause_duration)

    move_velocity_message_factory(vehicle, 0, velocity_y, velocity_duration)

    time.sleep(pause_duration)

    move_velocity_message_factory(vehicle, -(velocity_x), 0, velocity_duration)

    time.sleep(pause_duration)

    move_velocity_message_factory(vehicle, 0, -(velocity_y), velocity_duration)
