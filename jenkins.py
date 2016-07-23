#!/usr/bin/env python
import requests
import pprint
import json
import argparse
from config import config
from pkg_resources import resource_string

parser = argparse.ArgumentParser()
parser.add_argument("branch")
args = parser.parse_args()


def get_master_config():
    """
    Gets the config.xml file for the Jenkins build job for origin/master."""

    job_get_url = config['jenkins_url'] + "/job/" + config['master_job'] + "/config.xml"

    auth = (config['username'], config['api_key'])

    headers = {'Content-Type': 'application/xml'}

    response = requests.get(job_get_url, auth=auth, headers=headers)

    return(response.text)


master_config = get_master_config()

branch_config = master_config.replace("origin/master", args.branch)

job_create_url = config['jenkins_url'] + "/createItem"

auth = (config['username'], config['api_key'])

params = {'name': args.branch}

headers = {'Content-Type': 'application/xml'}

response = requests.post(job_create_url,
                         auth=auth,
                         headers=headers,
                         params=params,
                         data=branch_config)

print(response.status_code)
print(response.text)
