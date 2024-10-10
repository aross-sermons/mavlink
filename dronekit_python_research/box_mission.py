from utils import quad_utils
import time

def execute_box_mission_velocity(vehicle, mission:dict):
    """
    Executes the box mission with the given mission parameters in dictionary format.
    List of dictionary parameters:
        'takeoff_altitude': int
        'velocity_x': int
        'velocity_y': int
        'velocity_duration': int
        'pause_duration': int

    :param mission: The mission in dictionary format.
    """

    quad_utils.arm_message_factory(vehicle)

    quad_utils.set_mode_message_factory(vehicle, 'GUIDED')

    quad_utils.takeoff_message_factory(vehicle, mission['takeoff_altitude'])

    time.sleep(mission['pause_duration'])

    quad_utils.box_mission_velocity(vehicle, 
                                    velocity_x=mission['velocity_x'],
                                    velocity_y=mission['velocity_y'],
                                    velocity_duration=mission['velocity_duration'],
                                    pause_duration=mission['pause_duration'])
    
    time.sleep(mission['pause_duration'])

    quad_utils.land_message_factory(vehicle)

    quad_utils.set_mode_message_factory(vehicle, 'STABILIZE')

if __name__ == '__main__':
    box_mission = {
        'takeoff_altitude': 20,
        'velocity_x': 5,
        'velocity_y': 5,
        'velocity_duration': 5,
        'pause_duration': 10
    }

    vehicle = quad_utils.get_vehicle('tcp:127.0.0.1:5763')

    start_time = time.time()

    execute_box_mission_velocity(vehicle, mission=box_mission)

    end_time = time.time()

    trip_time = end_time - start_time

    print(f'Trip time: {trip_time}')