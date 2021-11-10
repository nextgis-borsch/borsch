#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Purpose: Script to create/recreate tag/release in repo
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Copyright (c) 2019 NextGIS <info@nextgis.com>
## License: GPL v.2
##
################################################################################

import os
import subprocess, shlex
import sys
import argparse
import json
import base64
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

repka_endpoint = 'https://rm.nextgis.com'
repo_id = 2
# Debug
# repka_endpoint = 'http://localhost:8088'
# repo_id = 1

class PutRequest(urllib2.Request):
    '''class to handling putting with urllib2'''

    def __init__(self, *args, **kwargs):
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        return 'PUT'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKGRAY = '\033[0;37m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DGRAY='\033[1;30m'
    LRED='\033[1;31m'
    LGREEN='\033[1;32m'
    LYELLOW='\033[1;33m'
    LBLUE='\033[1;34m'
    LMAGENTA='\033[1;35m'
    LCYAN='\033[1;36m'
    WHITE='\033[1;37m'

def color_print(text, bold, color):
    if sys.platform == 'win32':
        print(text)
    else:
        out_text = ''
        if bold:
            out_text += bcolors.BOLD
        if color == 'GREEN':
            out_text += bcolors.OKGREEN
        elif color == 'LGREEN':
            out_text += bcolors.LGREEN
        elif color == 'LYELLOW':
            out_text += bcolors.LYELLOW
        elif color == 'LMAGENTA':
            out_text += bcolors.LMAGENTA
        elif color == 'LCYAN':
            out_text += bcolors.LCYAN
        elif color == 'LRED':
            out_text += bcolors.LRED
        elif color == 'LBLUE':
            out_text += bcolors.LBLUE
        elif color == 'DGRAY':
            out_text += bcolors.DGRAY
        elif color == 'OKGRAY':
            out_text += bcolors.OKGRAY
        else:
            out_text += bcolors.OKGRAY
        out_text += text + bcolors.ENDC
        print(out_text)

def get_repo_name(repo):
    p = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=repo)
    base=os.path.basename(p)
    return os.path.splitext(base)[0]

def get_packet_id(packet_name, username, password):
    url =  repka_endpoint + '/api/packet?repository={}&filter={}'.format(repo_id, packet_name)
    color_print('Check packet url: ' + url, False, 'OKGRAY')
    request = urllib2.Request(url)
    
    if username is not None and password is not None:
        base64string = base64.b64encode('{}:{}'.format(username, password).encode("utf-8"))
        request.add_header("Authorization", "Basic %s" % base64string)   

    response = urllib2.urlopen(request)
    packets = json.loads(response.read())
    for packet in packets:
        if packet['name'] == packet_name: 
            return packet['id']
    return -1

def get_release(packet_id, tag, username, password):
    url =  repka_endpoint + '/api/release?packet={}'.format(packet_id)
    color_print('Check release url: ' + url, False, 'OKGRAY')
    request = urllib2.Request(url)
    
    if username is not None and password is not None:
        base64string = base64.b64encode('{}:{}'.format(username, password).encode("utf-8"))
        request.add_header("Authorization", "Basic %s" % base64string)   

    response = urllib2.urlopen(request)
    releases = json.loads(response.read())
    if releases is None:
        color_print('Release ID not found', False, 'LCYAN')
        return None

    for release in releases:
        if tag in release['tags']: 
            color_print('Release ID {} found'.format(release['id']), False, 'LCYAN')
            return release

    color_print('Release ID not found', False, 'LCYAN')
    return None

def upload_file(file_path, username, password):
    post_url = repka_endpoint + '/api/upload'
    args = ['curl', '-u', username + ':' + password, '-F', 'file=@' + file_path, 
        post_url
    ]
    load_response = subprocess.check_output(args)
    response = json.loads(load_response)

    print(response)

    file_uid = response['file']
    file_name = response['name']
    color_print('Uploaded: {} / {}'.format(file_uid, file_name), True, 'LGREEN')

    return file_uid, file_name

def create_release(packet_id, name, description, tag, file_uid, file_name, username, password):
    url = repka_endpoint + '/api/release'

    data = json.dumps({
        "name": name,
        "description": description,
        "tags": [tag, 'latest',],
        "packet": packet_id,
        "files": [
            {"upload_name": file_uid, "name": file_name},
        ]
    })
    clen = len(data)

    request = urllib2.Request(url, data=data, headers={'Content-Type': 'application/json', 'Content-Length': clen})
    
    if username is not None and password is not None:
        base64string = base64.b64encode('%s:%s' % (username, password))
        request.add_header("Authorization", "Basic %s" % base64string)   

    response = urllib2.urlopen(request)
    release = json.loads(response.read())

    color_print('Release with ID {} created'.format(release['id']), False, 'LCYAN')

    return release['id']

def update_release(release, file_uid, file_name, username, password):
    url = repka_endpoint + '/api/release/{}'.format(release['id'])
    color_print('Update release url: ' + url, False, 'OKGRAY')

    # Check if file exists
    is_exists = False
    if release['files']:
        for file in release['files']:
            if file['name'] == file_name:
                is_exists = True
                file['id'] = None
                file['upload_name'] = file_uid
                file['name'] = file_name
    if is_exists == False:
        file = {
            'name': file_name,
            'upload_name': file_uid
        }
        if release['files']:
            release['files'].append(file)
        else:
            release = [file]      

    data = json.dumps(release)

    print(data)

    clen = len(data)

    request = PutRequest(url, data=data, headers={'Content-Type': 'application/json', 'Content-Length': clen})
    
    if username is not None and password is not None:
        base64string = base64.b64encode('%s:%s' % (username, password))
        request.add_header("Authorization", "Basic %s" % base64string)   

    response = urllib2.urlopen(request)
    release = json.loads(response.read())

    color_print('Release updated. {}'.format(release['message']), True, 'LGREEN')

def do_work(repo_path, build_path, login, password):
    color_print('Repo: ' + repo_path + ', Build dir: ' + build_path, True, 'OKGRAY')

    with open(os.path.join(build_path, 'version.str')) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    tag = content[0]
    release_file = os.path.join(build_path, content[2]) + '.zip'
    
    packet_name = str(get_repo_name(repo_path))

# 1. Get packet ID
    packet_id = get_packet_id(packet_name, login, password)
    if packet_id == -1:
        color_print('Packet {} not found in repository'.format(packet_name), True, 'LRED')
        exit(1)

# 2. Upload file
    file_uid,file_name = upload_file(release_file, login, password)

# 3. Get release by tag
    release = get_release(packet_id, tag, login, password)

# 4. If no release - create it, else - update    
    release_name = tag
    release_desc = 'Version ' + tag
    if release is None:
        # Create new release
        create_release(packet_id, release_name, release_desc, tag, file_uid, file_name, login, password)
    else:
        # Update current release
        update_release(release, file_uid, file_name, login, password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NextGIS Borsch tools. Utility to create or recreate release in repository')
    parser.add_argument('-v', '--version', action='version', version='NextGIS Borsch repka_release version 1.0')
    parser.add_argument('--login', dest='login', help='repka login')
    parser.add_argument('--password', dest='password', help='repka password')
    parser.add_argument('--repo_path', dest='repo', help='path to repository on disk')
    parser.add_argument('--build_path', dest='build', help='build directory to search version.str and upload zip files')

    args = parser.parse_args()

    if args.repo:
        repo_path = args.repo
        build_path = args.build
    else:
        repo_path = os.getcwd()
        build_path = os.path.join(repo_path, args.build)

    do_work(repo_path, build_path, str(args.login), str(args.password))
