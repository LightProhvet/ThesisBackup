import threading

from .odrive_connection import ODriveConnection
from .odrive_axes_of import is_odrv_enabled

#odrive_ids = [35576160596046, 35623406219342]
#odrive_ids = [35679242498126] # development board with some broken transistors3
odrive_ids = ['/dev/odrive0', '/dev/odrive1']
#odrive_ids = ['/dev/odrive0']
#odrive_ids = ['/dev/odrive1']
"""
Odrives connections to motors
odrive0 - 35576160596046 - connected in hub port closest to the hub cable
M0 - rear left
M1 - front left
odrive1 - 35623406219342 - connected in hub middle port
M0 - front right
M1 - rear right
"""

def connect_odrives():
    parallel = True

    odrv_dict = dict()

    def connect_odrive_by_id(odrive_id):
        print('Connecting to ODrive {}...'.format(odrive_id))
        conn = ODriveConnection('uart', odrive_id).create_conn()
        if type(conn.odrv) != type(None):
            odrv_dict[odrive_id] = conn
            print('Connected to ODrive {}!'.format(odrive_id))

    if parallel:
        threads = []
        # Connect only to ODrives for which at least one axis is enabled
        for odrive_id in filter(is_odrv_enabled, odrive_ids):
            thr = threading.Thread(target = connect_odrive_by_id, args = (odrive_id,))
            thr.start()
            threads.append(thr)

        for thr in threads:
            thr.join()
    else:
        for odrive_id in filter(is_odrv_enabled, odrive_ids):
            connect_odrive_by_id(odrive_id)

    return [odrv_dict[odrive_id] for odrive_id in odrive_ids if odrive_id in odrv_dict and is_odrv_enabled(odrive_id)]
