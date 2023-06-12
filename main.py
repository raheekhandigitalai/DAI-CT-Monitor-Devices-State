import os.path

import APIs
import helpers
from APIs import get_device_list
from APIs import run_http_request

from helpers import write_to_file
from helpers import create_folder
from helpers import logger

import concurrent.futures


def process_device(device_info):
    device_property = device_info.split('|')
    device_properties = f'{device_property[0]} | {device_property[1]} | {device_property[2]} | {device_property[3]}'

    if 'Offline' in device_info:
        logger(f'Device Properties: {device_properties}')
        return 'offline', device_properties

    if 'Available' in device_info:
        logger(f'Device Properties: {device_properties}')
        http_result = run_http_request(device_property[0])
        return 'online', device_properties, http_result

    if 'In Use' in device_info:
        logger(f'Device Properties: {device_properties}')
        http_result = run_http_request(device_property[0])
        return 'in_use', device_properties, http_result

    if 'Error' in device_info:
        logger(f'Device Properties: {device_properties}')
        return 'error', device_properties

    if 'Unauthorized' in device_info:
        logger(f'Device Properties: {device_properties}')
        return 'unauthorized', device_properties

    logger(f'Device Properties: {device_properties}')
    return 'not_sure', device_properties


def check_if_device_is_connected_to_the_internet():
    # Get list of Devices using from SeeTest Cloud
    devices = get_device_list()

    # Creating empty lists to be populated based on devices Status
    rows_offline = []
    rows_online = []
    rows_in_use = []
    rows_error = []
    rows_unauthorized = []
    rows_not_sure = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for device in devices:
            futures.append(executor.submit(process_device, device))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()

            # not all devices has http_result value, causing an error when there are only two values returned from future.result()
            # TO handle this situation, following check has been added
            if len(result) == 2:
                status, properties = result
                http_result = None
            else:
                status, properties, http_result = result

            if status == 'offline':
                rows_offline.append(properties)
            elif status == 'online':
                rows_online.append(properties)
                if http_result:
                    rows_online.append(http_result)
                rows_online.append('================================================')
            elif status == 'in_use':
                rows_in_use.append(properties)
                if http_result:
                    rows_in_use.append(http_result)
                rows_in_use.append('================================================')
            elif status == 'error':
                rows_error.append(properties)
            elif status == 'unauthorized':
                rows_unauthorized.append(properties)
            else:
                rows_not_sure.append(properties)

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

