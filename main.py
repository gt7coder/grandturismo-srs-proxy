"""
This python scripts collects the telemetry from the GT Sports and GT7
And sends it to the Sim Racing Studio API

All the credits go to Nenkai to that was able to figure out how to decrypt the telemetry
packets from the game:
https://github.com/Nenkai/PDTools/tree/master/PDTools.SimulatorInterface
I encourage you to donate for him!

We can now finally use Wind Simulators, Shakers, Rumble and Motion platforms from
DOFReality, ProSimu, PT-Actuator, SFX-100 (With Thanos Controller) and YawVR

I am not affiliated to SimRacingStudio
I am not responsible for any damage that this could case to you or your equipment

Keep in mind that this is an undocumented API from Grand Turismo, they match patch
and close the door in the future.

Enjoy!
"""

import socket
import sys
from gt_packet_definition import GTDataPacket
import pure_salsa20
import struct
import ctypes
import argparse
from ipaddress import ip_address
from srs_packet_definition import TelemetryPacket, PACKET_HEADER, API_VERSION

game_definition = {'gt7': {'key': b'Simulator Interface Packet GT7 ver 0.0', 'bind_port': 33740, 'receive_port': 33739},
                   'gtsport': {'key': b'Simulator Interface Packet ver 0.0', 'bind_port': 33340, 'receive_port': 33339}}

'test'[:32]

parser = argparse.ArgumentParser()
parser.add_argument("--playstation_ip",
                    required=True,
                    type=str,
                    help="Playstation 4/5 IP address, to find the playstation IP address select the P button the "
                         "gamepad, go to settings, network, view connections status, e.g. 192.168.0.2")

parser.add_argument("--srs_ip",
                    type=str,
                    default='127.0.0.1',
                    help="IP of the computer where srs is running, to find the IP address, open the SimRacingStudio App"
                         ", navigate to Setup -> App -> Network IP")

parser.add_argument("--srs_port",
                    type=int,
                    default=33001,
                    help="Port where the SRS is expecting to receive telemetry, it can be changed on the "
                         "\\documents\\SimRacingStudio 2.0\\config.ini [NETWORK_PORT] api")


def decrypt(key, data):
    key = key[:32]

    try:
        iv1 = struct.unpack("<i", bytes(data[64:68]))[0]
        iv2 = ctypes.c_int32(iv1 ^ 0xDEADBEAF)
        iv = struct.unpack("<BBBB", iv2) + tuple(struct.pack("<i", iv1))
        decrypted = pure_salsa20.salsa20_xor(key, iv, data)
    except Exception as e:
        print('Failed to decrypt data')
        return b''

    return decrypted


if __name__ == "__main__":

    args = parser.parse_args()

    for ip in (args.playstation_ip, args.srs_ip):
        try:
            ip_address(ip)
        except (ValueError, TypeError) as e:
            print('The ' + ip + ' is not a valid IP Address')
            sys.exit()

    srs_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srs_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srs_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    srs_client_address = (args.srs_ip, args.srs_port)

    while True:
        for key, value in game_definition.items():

            print('Checking if ' + key + ' is running...')

            try:
                playstation_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                playstation_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            except Exception as e:
                print('Invalid instance of socket', str(e))

            try:
                playstation_socket.bind(('', value['bind_port']))
                playstation_socket.settimeout(5)
            except Exception as e:
                print('socket error', str(e))
                continue

            while True:

                try:
                    playstation_socket.sendto(b'A', (args.playstation_ip, value['receive_port']))
                except Exception as e:
                    print('error sending initialization packet to ', str(e))
                    break

                try:
                    data, addr = playstation_socket.recvfrom(296)  # receiving from socket
                except Exception as e:
                    print('error sending receiving packet from ', key, str(e))
                    break

                if len(data) == 296:
                    decrypted_data = decrypt(value['key'], data)
                    if len(data) == 296:
                        telemetry = GTDataPacket(decrypted_data[0:252])
                        if telemetry.magic == 0x47375330:

                            srs_packet = TelemetryPacket(PACKET_HEADER,
                                                         API_VERSION,
                                                         str.encode(key),
                                                         str.encode('NA'),
                                                         str.encode('NA'),
                                                         telemetry.speed,
                                                         telemetry.rpm,
                                                         telemetry.min_alert_rpm,
                                                         telemetry.bits & 0b1111,
                                                         telemetry.pitch * 50,
                                                         telemetry.roll * -50, #need to reverse srs is expecting other side
                                                         telemetry.yaw * 50,
                                                         0,  # this is required for traction loss, need to find it
                                                         telemetry.acceleration_y * -50, #need to reverse
                                                         telemetry.acceleration_z * 50,
                                                         telemetry.acceleration_x * 50,
                                                         0, #need to find the suspension travel for bumps
                                                         0,
                                                         0,
                                                         0,
                                                         0, #need to find the terrain surface of the wheel
                                                         0,
                                                         0,
                                                         0,
                                                         )

                            try:
                                is_on_track = (telemetry.flags & 1) > 0
                                is_paused = (telemetry.flags & 2) > 0
                            except:
                                print('failed to decode the gt flags')
                                is_on_track = False
                                is_paused = True
                                break

                            if is_on_track and is_paused is False: #only sends the telemetry to SRS if the car is on track and the game is not on the pause menu
                                try:
                                    srs_socket.sendto(srs_packet, srs_client_address)
                                except Exception as e:
                                    print('Error sending telemetry to SRS ', str(e))

                            print('is_on_track', is_on_track, 'is_paused', is_paused, 'rpm', telemetry.rpm, 'gear', telemetry.bits & 0b1111, 'speed', telemetry.speed)

                        else:
                            print('error decrypting the data from, this is not a valid magic', key)
                    else:
                        print('error decrypting the data from ', key)
                        break
                else:
                    print('This is not a valid packet for ' + key)
                    break
