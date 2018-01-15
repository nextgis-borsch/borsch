#!/usr/bin/python

# Script to create/recreate tag/release in repo

import os
import subprocess, shlex
import sys
import argparse
import urllib2, json
import base64

github_endpoint = 'https://api.github.com'

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
        print text
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
        print out_text

def check_tag_exist(tag, repo):
    subprocess.check_output(['git', 'fetch', '--tags'], cwd=repo)
    p = subprocess.check_output(['git', 'tag', '-l', 'v*'], cwd=repo)
    return tag in p.splitlines()

def check_release(tag, repo, release_file, username, password):
    color_print('Check release ' + tag, True, 'OKGRAY')
    remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=repo)
    remote_repo = os.path.splitext(os.path.basename(remote_url))[0]
    url =  github_endpoint + '/repos/nextgis-borsch/' + remote_repo + '/releases'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    releases = json.loads(response.read())
    for release in releases:
        if release['tag_name'] == tag:
            color_print('Release ' + tag + ' found', False, 'LCYAN')
            assets_url = release['upload_url']
            assets = release['assets']
            release_file_name = os.path.basename(release_file)
            for asset in assets:
                if asset['name'] == release_file_name:
                    # Delete asset
                    base64string = base64.b64encode('%s:%s' % (username, password))
                    auth = "Basic " + base64string
                    color_print('Delete asset ' + release_file_name + ' [' + asset['url'] + ']', False, 'LRED')
                    request = urllib2.Request(asset['url'], headers={'Authorization' : auth})
                    request.get_method = lambda: 'DELETE'
                    response = urllib2.urlopen(request)
                    break
            return assets_url
    return None

def create_release(tag, repo, username, password):
    color_print('Create release ' + tag, False, 'LGREEN')
    remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=repo)
    remote_repo = os.path.splitext(os.path.basename(remote_url))[0]
    url =  github_endpoint + '/repos/nextgis-borsch/' + remote_repo + '/releases'
    data = json.dumps({
        "tag_name": tag,
        "target_commitish": "master",
        "name": tag,
        "body": "Version " + tag,
        "draft": False,
        "prerelease": False})
    clen = len(data)

    base64string = base64.b64encode('%s:%s' % (username, password))
    auth = "Basic " + base64string
    request = urllib2.Request(url, data=data, headers={'Content-Type': 'application/json', 'Content-Length': clen, 'Authorization' : auth})
    response = urllib2.urlopen(request)
    releases = json.loads(response.read())

    return releases['upload_url']

def upload_release(url, release_file, username, password):
    color_print('Upload release file ' + release_file, True, 'LGREEN')
    file_name = os.path.basename(release_file)
    post_url = url.replace('{?name,label}', '?name=') + file_name
    args = ['curl', '-u', username + ':' + password, '-H', 'Content-Type: application/zip', '--data-binary', '@' + release_file, post_url]

    load_response = subprocess.check_output(args)

    response = json.loads(load_response)

    color_print('Uploaded. Get it: ' + response['browser_download_url'], True, 'LGREEN')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NextGIS Borsch tools. Utility to create or recreate release in repository')
    parser.add_argument('-v', '--version', action='version', version='NextGIS Borsch github_release version 1.0')
    parser.add_argument('--login', dest='login', help='github.com login')
    parser.add_argument('--key', dest='key', help='github.com access key')
    parser.add_argument('--repo_path', dest='repo', help='path to repository on disk')
    parser.add_argument('--build_path', dest='build', help='release file to upload')

    args = parser.parse_args()

    login = args.login
    key = args.key
    repo_path = args.repo
    build_path = args.build

    with open(os.path.join(build_path, 'version.str')) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    tag = 'v' + content[0]
    release_file = os.path.join(build_path, content[2]) + '.zip'

# 1. Check if tag created in repo
    if(not check_tag_exist(tag, repo_path)):
# 2. If not create - exit with error
        color_print('Tag {} is not created in repositry'.format(tag), True, 'LRED')
        exit(1)
# 3. Check if release created from tag
    upload_url = check_release(tag, repo_path, release_file, login, key)
    if upload_url is None:
# 4. If not created - create it
        upload_url = create_release(tag, repo_path, login, key)
# 5. Upload asset to github
    upload_release(upload_url, release_file, login, key)
