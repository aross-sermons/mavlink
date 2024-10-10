import box_mission
from utils import quad_utils
from utils import encrypt_decrypt_aes as aes
import time
import json
import os

def log_trip_times(unencrypted_trip_times:list, encrypted_trip_times:list, encryption_times:list, decryption_times:list):
    """
    Function for calculating the mean of trip times and logging them.

    :param unencrypted_trips: A list of times of each unencrypted trip.
    :param encrypted_trips: A list of times of each encrypted trip.
    """
    unencrypted_trips_mean = (sum(unencrypted_trip_times) / len(unencrypted_trip_times))
    encrypted_trips_mean = (sum(encrypted_trip_times) / len(encrypted_trip_times))
    encryption_times_mean = (sum(encryption_times) / len(encryption_times))
    decryption_times_mean = (sum(decryption_times) / len(decryption_times))

    # Find the last log file so a new log file can be created.
    log_num = 1
    while os.path.exists(f'./logs/aes_times{log_num}.txt'):
        log_num += 1
    
    # Create a new log file and print trip time information.
    with open(f'./logs/aes_times{log_num}.txt', 'w') as new_file:
        new_file.write("Mission, encryption, and decryption times in seconds:\n\n")
        new_file.write(f'unencrypted times: {unencrypted_trip_times}\n')
        new_file.write(f'unencrypted mean: {unencrypted_trips_mean}\n')
        new_file.write(f'encrypted times: {encrypted_trip_times}\n')
        new_file.write(f'encrypted mean: {encrypted_trips_mean}\n\n')
        new_file.write(f'encryption times: {encryption_times}\n')
        new_file.write(f'encryption times mean: {encryption_times_mean}\n')
        new_file.write(f'decryption times: {decryption_times}\n')
        new_file.write(f'decryption times mean: {decryption_times_mean}')

    print(f'Trip times printed to \"aes_times{log_num}.txt\".')

def execute_missions(missions:int=5):
    """
    Function to run missions number of box missions with and without AES encryption.
    Calculates the time each mission takes and adds it to a list.

    :param missions: The number of missions for each encryption method. Multiply by 2 for total number of missions.
    """
    unencrypted_mission_times = []
    encrypted_mission_times = []
    encryption_times = []
    decryption_times = []

    # Get the vehicle to run missions on.
    connection_string = 'tcp:127.0.0.1:5760'
    vehicle = quad_utils.get_vehicle(connection_string)

    # AES encryption parameters.
    key_size = 32
    iv_size = 16
    aes_key = aes.generate_aes_key(key_size)

    # Box mission parameters.
    box_mission_params = {
        'takeoff_altitude': 10,
        'velocity_x': 3,
        'velocity_y': 3,
        'velocity_duration': 3,
        'pause_duration': 5
    }

    # Loop to execute unencrypted box mission.
    for i in range(1, (missions+1)):
        print("#########################################################################")
        print(f'Starting unencrypted trip #{i}/{(missions)}:')

        mission_start_time = time.time()

        box_mission.execute_box_mission_velocity(vehicle, box_mission_params)

        mission_end_time = time.time()

        mission_time = mission_end_time - mission_start_time
        mission_time = round(mission_time, 2)

        unencrypted_mission_times.append(mission_time)

        print(f'Finished unencrypted trip #{i}/{(missions)} in {mission_time} seconds.')
        print("#########################################################################")

    # Loop to execute encrypted box mission.
    for i in range(1, (missions+1)):
        print("#########################################################################")
        print(f'Starting encrypted trip #{i}/{(missions)}:')
        
        encryption_start_time = time.perf_counter()

        encrypted_box_mission = aes.encrypt_data(json.dumps(box_mission_params), aes_key, iv_size)

        encryption_end_time = time.perf_counter()
        decryption_start_time = time.perf_counter()

        decrypted_box_mission = aes.decrypt_data(encrypted_box_mission, aes_key, iv_size)

        decrypted_box_mission = json.loads(decrypted_box_mission.decode('utf-8'))

        decryption_end_time = time.perf_counter()
        mission_start_time = time.time()

        box_mission.execute_box_mission_velocity(vehicle, mission=decrypted_box_mission)

        mission_end_time = time.time()

        encryption_time = encryption_end_time - encryption_start_time
        #encryption_time = round(encryption_time, 2)
        encryption_times.append(encryption_time)

        decryption_time = decryption_end_time - decryption_start_time
        #decryption_time = round(decryption_time, 2)
        decryption_times.append(decryption_time)

        mission_time = mission_end_time - mission_start_time
        mission_time = round(mission_time, 2)
        encrypted_mission_times.append(mission_time)

        print(f'Finished encrypted trip #{i}/{(missions)} in {mission_time} seconds.')
        print(f'Encrypted mission in {encryption_time} seconds.')
        print(f'Decrypted mission in {decryption_time} seconds.')
        print("#########################################################################")

    vehicle.close()

    log_trip_times(unencrypted_mission_times, encrypted_mission_times, encryption_times, decryption_times)

if __name__ == "__main__":
    execute_missions(10)