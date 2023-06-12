import configparser
from datetime import datetime
import os

config = configparser.ConfigParser()
config.read('config.properties')


def get_current_date_and_time():
    now = datetime.now()
    current_date_and_time = now.strftime("%m_%d_%Y-%H_%M_%S")
    return current_date_and_time


def create_folder():
    folder_name = 'devices_state_' + get_current_date_and_time()
    os.mkdir(folder_name)
    return folder_name


def write_to_file(folder_name, file_name, items):
    if items:  # Check if the list is not empty
        with open(folder_name + '/' + file_name + '-' + get_current_date_and_time() + '.txt', 'w') as f:
            for item in items:
                f.write("%s\n" % item)


def logger(message):
    print(message)


def get_access_key():
    return config.get('seetest_authorization', 'access_key')


def get_cloud_url_and_devices_end_point():
    return config.get('seetest_urls', 'cloud_url') + config.get('seetest_urls', 'end_point')


def url_to_hit_for_connectivity_status():
    return config.get('url_to_hit_for_connectivity_status', 'url_to_hit')
