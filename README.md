## Script for understanding Devices State

Digital.ai has developed an API that allow Cloud Admins to perform HTTP request on a Mobile Device (iOS & Android), and get the HTTP response in return. 

This script was designed to leverage the API to perform a GET request against a Public Website. This allows us to understand if the Device is connected to the Internet or not. When you have a large amount of Mobile Devices, this becomes like a monitoring tool.

The API also captured Error Messages if the device is in a problematic state, which may potentially cause issues to the user (_E.g., unable to open Device reflection, even after showing device as 'Online'_).

### API Information

POST: api/v1/devices/<device_id>/http-request

body parameters:
- **method** (optional): GET (GET by default)
- **url** (mandatory) - http/https address 
- **headers** (optional): list of key values for the header 
- **body** (optional) - binary 
- **timeout** (optional) - by default 5 seconds.

The API can be triggered even if the Mobile Device is currently being used by a user. This means Cloud Admins can run this script periodically without it affecting user sessions, as this runs in the background as a hidden process.

To see the code logic, look at method "**run_http_request**" under "**APIs.py**" file.

### Flow of the Script

This is the flow of the script and what it does when triggered:

- Get list of all devices from a SeeTest Cloud 
- Get state of devices
- If device is in 'offline', 'error' or 'unauthorized' state
  - Write it into separate .txt files for each state in a new folder under the root project directory 
- If device is  in 'online' or 'in use' state 
    - Run HTTP Request to ping against a website and write it into a .txt file in root project folder

&nbsp;

For now the script logic is only written so far, but further improvements can be made, such as:
- If a device is in bad state, label the devices appropriately. Labels are visible in the Continuous Testing UI
- If a device is in bad state, send a Slack message or an Email to CloudOps / Network / Security Teams,
- If a device is in bad state, take appropriate actions (E.g., [Reboot Device with API](https://docs.experitest.com/display/PM/Devices+Rest+API#DevicesRestAPI-RebootDevice))

### Prerequisites

**config.properties** needs to be updated to provide the following information:

```
[seetest_authorization]
access_key=<insert access key>

[seetest_urls]
cloud_url=https://uscloud.experitest.com # replace with your Cloud URL
```

[Obtain your Access Key](https://docs.experitest.com/display/TE/Obtaining+Access+Key)

### How to set up environment

Open a Terminal window in the project root folder, and type in the following commands:

```commandline
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Above steps creates a local virtual environment where Python3, Pip3 and all relevant dependencies reside. 

To run the script, running the following command:

```commandline
./env/bin/python3 main.py
```
