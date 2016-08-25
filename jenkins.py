#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import requests
import argparse
from config import config

parser = argparse.ArgumentParser()
parser.add_argument("branch")
parser.add_argument("email", default=None)
parser.add_argument("username")
parser.add_argument("password")
args = parser.parse_args()


def get_master_config():
    """
    Gets the config.xml file for the Jenkins build job for origin/master.
    """
    job_get_url = "{}/job/{}/config.xml".format(config['jenkins_url'],
                                                config['master_job'])

    auth = (args.username, args.password)

    headers = {'Content-Type': 'application/xml'}

    response = requests.get(job_get_url, auth=auth, headers=headers)

    return response.text


def main():
    master_config = get_master_config()

    branch_config = master_config.replace("origin/master", args.branch)

    if args.email is not None:
        branch_config = branch_config.replace(
                            "<recipients></recipients>",
                            "<recipients>{}</recipients>".format(args.email))

    print(branch_config)

    job_create_url = config['jenkins_url'] + "/createItem"

    auth = (args.username, args.password)

    params = {'name': args.branch}

    headers = {'Content-Type': 'application/xml'}

    response = requests.post(job_create_url,
                             auth=auth,
                             headers=headers,
                             params=params,
                             data=branch_config)

    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    main()
