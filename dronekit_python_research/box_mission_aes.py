from utils import quad_utils
from utils import encrypt_decrypt_aes as aes
import box_mission
import json
import time

if __name__ == '__main__':
    box_mission = {
        'takeoff_altitude': 20,
        'velocity_x': 5,
        'velocity_y': 5,
        'velocity_duration': 5,
        'pause_duration': 10
    }

    key_size = 32
    iv_size = 16
    aes_key = aes.generate_aes_key(key_size)

    vehicle = quad_utils.get_vehicle('tcp:127.0.0.1:5763')

    start_time = time.time()

    encrypted_box_mission = aes.encrypt_data(json.dumps(box_mission), aes_key, iv_size)

    decrypted_box_mission = aes.decrypt_data(encrypted_box_mission, aes_key, iv_size)

    decrypted_box_mission = json.loads(decrypted_box_mission.decode('utf-8'))

    box_mission.execute_box_mission_velocity(vehicle, mission=decrypted_box_mission)

    end_time = time.time()

    trip_time = end_time - start_time

    print(f'Trip time: {trip_time}')