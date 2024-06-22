from mavdefs import universal_defs
from pymavlink.dialects.v10.python2 import ardupilotmega as mavlink

vehicle = universal_defs.get_vehicle('tcp:127.0.0.1:5760')\


# msg = vehicle.message_factory.heartbeat_encode(
#         type=mavlink.MAV_TYPE_GCS,
#         autopilot=mavlink.MAV_AUTOPILOT_INVALID,
#         base_mode=0,
#         custom_mode=0,
#         system_status=mavlink.MAV_STATE_ACTIVE
#     )

print("Roundtrip Time: %s" % universal_defs.measure_round_trip(vehicle))

# msg = vehicle.message_factory.command_long_encode(
#         0, 0,  # target system, target component
#         mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # command
#         0,  # confirmation
#         1,  # param1 (1 to arm, 0 to disarm)
#         0, 0, 0, 0, 0, 0  # unused parameters
#     )

# print("Roundtrip Time: %s" % universal_defs.measure_round_trip(vehicle, msg, 'armed'))