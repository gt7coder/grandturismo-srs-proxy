'''
Sim Racing Studio API.
'''
from ctypes import *

# definition of the constants
PACKET_HEADER = str.encode('api')  # constant to identify the package
API_VERSION = 102  # constant of the current version of the api

# defition of the Telemetry Class
class TelemetryPacket(Structure):
    _fields_ = [('api_mode', c_char * 3),  # 'api' constant to identify packet
                ('version', c_uint),  # version value = 102
                ('game', c_char * 50),  # Game name for example Project Cars 2
                ('vehicle_name', c_char * 50),  # car, boar or aircraft name
                ('location', c_char * 50),  # track name, location, airport, etc
                ('speed', c_float),  # float
                ('rpm', c_float),  # float
                ('max_rpm', c_float),  # float
                ('gear', c_int),  # -1 = revere 0=Neutral 1 to 9=gears
                ('pitch', c_float),  # in degrees -180 to +180
                ('roll', c_float),  # in degrees -180 to +180
                ('yaw', c_float),  # in degrees -180 to +180
                ('lateral_velocity', c_float),  # in float between -2 to 2 used for traction loss
                ('lateral_acceleration', c_float),  # gforce in float values beteween 0 to 10
                ('vertical_acceleration', c_float),  # gforce in float values beteween 0 to 10
                ('longitudinal_acceleration', c_float),  # gforce in float values beteween 0 to 10
                ('suspension_travel_front_left', c_float),  # in float values -10 to 10
                ('suspension_travel_front_right', c_float),  # in float values -10 to 10
                ('suspension_travel_rear_left', c_float),  # in float values -10 to 10
                ('suspension_travel_rear_right', c_float),  # in float values -10 to 10
                ('wheel_terrain_front_left', c_uint),  # 0=all others, 1=rumble strip, 2=asphalt
                ('wheel_terrain_front_right', c_uint),  # 0=all others, 1=rumble strip, 2=asphalt
                ('wheel_terrain_rear_left', c_uint),  # 0=all others, 1=rumble strip, 2=asphalt
                ('wheel_terrain_rear_right', c_uint),  # 0=all others, 1=rumble strip, 2=asphalt
                ]
