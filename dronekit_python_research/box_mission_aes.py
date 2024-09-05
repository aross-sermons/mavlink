from utils import quad_utils
import time

vehicle = quad_utils.get_vehicle('tcp:127.0.0.1:5763')

start_time = time.time

quad_utils.arm_message_factory(vehicle)

quad_utils.set_mode_message_factory(vehicle, 'GUIDED')

quad_utils.takeoff_message_factory(vehicle, 20)

time.sleep(10)

quad_utils.move_velocity_message_factory(vehicle, 5, 0, 0, 5)

time.sleep(10)

quad_utils.move_velocity_message_factory(vehicle, 0, 5, 0, 5)

time.sleep(10)

quad_utils.move_velocity_message_factory(vehicle, -5, 0, 0, 5)

time.sleep(10)

quad_utils.move_velocity_message_factory(vehicle, 0, -5, 0, 5)

time.sleep(10)

quad_utils.land_message_factory(vehicle)

quad_utils.set_mode_message_factory(vehicle, 'STABILIZE')

end_time = time.time

print(f'Trip time: {end_time - start_time}')