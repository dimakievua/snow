import requests
import re
from os import getenv
from sys import exit
from kubernetes import client, config
from munch import munchify

ACTION = getenv('ACTION')
SNOWBASEURL = 'http://' + getenv('SNOWURL')
SNOWAPIURL = SNOWBASEURL + '/api/now/table/incident'

def validate_snow_endpoint(url):
    response = requests.get(
        url
    )
    return str(response.status_code)

def prepare_headers(action):
    if action == 'get':
       result = {"Accept":"application/json"}
    else:
       result =  {"Content-Type":"application/json","Accept":"application/json"}
    print(result)
    return result

def prepare_data(action):
    if action == 'post':
       result = '{"short_description":"Test"}'
    elif action == 'put':
       result = '{"short_description":"Test Update"}'
    elif action == 'patch':
       result = '{"short_description":"Test update Patch"}'
    else:
       result = ""
    print(result)
    return result

def do_request(url, headers, action, data, user, pwd):
    # Do the HTTP request
    response = getattr(requests, action)(
        url,
        auth=(user, pwd),
        headers=headers,
        data=data
    )
    return response

def verify_response_status(status_code):
    # Status codes 3** not processed here because in request methods by default we have parameter
    # allow_redirects = true, that means we can receive any status codes except 3**
    is_valid = re.findall("2\d.", status_code)
    return is_valid.count(status_code) != 0

try:
    user = 'admin'
    pwd = 'admin'
    if verify_response_status(validate_snow_endpoint(SNOWBASEURL)):
        print("Successfuly reached " + SNOWBASEURL)
        print(str(SNOWBASEURL + "/" + ACTION)) # this need only for httpbin test
        print(do_request(str(SNOWBASEURL + "/" + ACTION), prepare_headers(ACTION), ACTION, prepare_data(ACTION), user, pwd))
    else:
        raise Exception("Failed to reach endpoint " + SNOWURL)
except:
    print("Oops! Something went wrong.")
