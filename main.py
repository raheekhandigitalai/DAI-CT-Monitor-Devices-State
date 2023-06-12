import os.path

import APIs
import helpers
from APIs import get_device_list
from APIs import run_http_request

from helpers import write_to_file
from helpers import create_folder
from helpers import logger


def check_if_device_is_connected_to_the_internet():
    # Get list of Devices using from SeeTest Cloud
    device_info = get_device_list()

    # Creating empty lists to be populated based on devices Status
    rows_offline = []
    rows_online = []
    rows_in_use = []
    rows_error = []
    rows_unauthorized = []
    rows_not_sure = []

    # Check for each device retrieved
    for i in range(len(device_info)):
        device_property = device_info[i].split('|')
        # Separating out the individual device properties for better readability in the .txt files generated:
        # properties in order: device_id, device_status, device_name, device_udid
        device_properties = device_property[0] + ' | ' + device_property[1] + ' | ' + device_property[2] + ' | ' + device_property[3]

        if 'Offline' in device_info[i]:
            logger(f"Device Properties: {device_properties}")
            rows_offline.append(device_properties)
        elif 'Available' in device_info[i]:
            logger(f"Device Properties: {device_properties}")
            rows_online.append(device_properties)
            rows_online.append(run_http_request(device_property[0]))
            rows_online.append("================================================")
        elif 'In Use' in device_info[i]:
            logger(f"Device Properties: {device_properties}")
            rows_in_use.append(device_properties)
            rows_in_use.append(run_http_request(device_property[0]))
            rows_in_use.append("================================================")
        elif 'Error' in device_info[i]:
            logger(f"Device Properties: {device_properties}")
            rows_error.append(device_properties)
        elif 'Unauthorized' in device_info[i]:
            logger(f"Device Properties: {device_properties}")
            rows_unauthorized.append(device_properties)
        # Every other Status not defined
        else:
            rows_not_sure.append(device_properties)

    folder_path = create_folder()
    write_to_file(folder_path, 'offline_devices', rows_offline)
    write_to_file(folder_path, 'online_devices', rows_online)
    write_to_file(folder_path, 'in_use_devices', rows_in_use)
    write_to_file(folder_path, 'error_devices', rows_error)
    write_to_file(folder_path, 'unauthorized_devices', rows_unauthorized)
    write_to_file(folder_path, 'not_sure', rows_not_sure)


if __name__ == '__main__':
    check_if_device_is_connected_to_the_internet()
    # print(APIs.get_device_tags('2025017'))
    # print(run_http_request('2025017'))

