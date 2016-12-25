#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Copyright (c) 2016 NextGIS <info@nextgis.com>
## License: GPL v.2
##
################################################################################

import argparse
import os
import shutil
import string
import subprocess
import sys

repositories = [
    {"url" : "borsch", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_curl", "cmake_dir" : "CMake", "build" : [], "args" : ""},
    {"url" : "lib_openssl", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_tiff", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "lib_lzma", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "lib_hdf4", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_png", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "lib_geotiff", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "tests", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_xml2", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_hdfeos2", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_gdal", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "lib_pq", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_spatialite", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_iconv", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_freexl", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_spatialindex", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "postgis", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_geos", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_sqlite", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_proj", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_jsonc", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "lib_szip", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_jpeg", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "lib_z", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_jbig", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ""},
    {"url" : "lib_expat", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "googletest", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_boost", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_zip", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_uv", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_jpegturbo", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_variant", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_rapidjson", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_nunicode", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_geojsonvt", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_opencad", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_ecw", "cmake_dir" : "cmake", "build" : [], "args" : ""},
    {"url" : "lib_mrsid", "cmake_dir" : "cmake", "build" : [], "args" : ""},
]

args = {}

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
    DGRAY='\033[1;30m'     #  ${DGRAY}
    LRED='\033[1;31m'       #  ${LRED}
    LGREEN='\033[1;32m'     #  ${LGREEN}
    LYELLOW='\033[1;33m'     #  ${LYELLOW}
    LBLUE='\033[1;34m'     #  ${LBLUE}
    LMAGENTA='\033[1;35m'   #  ${LMAGENTA}
    LCYAN='\033[1;36m'     #  ${LCYAN}
    WHITE='\033[1;37m'     #  ${WHITE}

#print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC

def parse_arguments():
    global args

    parser = argparse.ArgumentParser(description='NextGIS Borsch tools.')
    subparsers = parser.add_subparsers(help='command help', dest='command')
    parser_git = subparsers.add_parser('git')
    parser_git.add_argument('--clone', action='store_true', help='clone all repositories')
    parser_git.add_argument('--pull', action='store_true', help='update all repositories')
    parser_git.add_argument('--status', action='store_true', help='print status of repositories')
    parser_git.add_argument('--push', action='store_true', help='send changes to server')
    parser_git.add_argument('--commit', dest='message', help='commit changes in repositories')

    parser_make = subparsers.add_parser('make')

    args = parser.parse_args()

def run(args):
    #print 'calling ' + string.join(args)
    subprocess.check_call(args)

def color_print(text, bold, color):
    if sys.platform == 'windows':
        print text
    else:
        out_text = ''
        if bold:
            out_text += bcolors.BOLD
        if color == 'GREEN':
            out_text += bcolors.OKGREEN
        elif color = 'LGREEN':
            out_text += bcolors.LGREEN
        elif color == 'LYELLOW':
            out_text += bcolors.LYELLOW        
        else:
            out_text += bcolors.OKGRAY
        out_text += text + bcolors.ENDC
        print out_text

def git_status():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        print color_print('status ' + repository['url'], True, 'LGREEN')
        os.chdir(repository['url'])
        run(('git', 'status'))
        os.chdir(os.path.join(os.getcwd(), os.pardir))

def git_pull():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        print color_print('pull ' + repository['url'], True, 'LYELLOW')
        os.chdir(repository['url'])
        run(('git', 'pull'))
        os.chdir(os.path.join(os.getcwd(), os.pardir))

    git_pull() {
        echo -e "${BOLD}${BGDEF}${LYELLOW} pull $1 ${NORMAL}"
        cd $1
        git pull && echo -e "${ALL_IS_OK_MSG}"
        cd ..
    }

parse_arguments()
if args.command == 'git':
    git_status()
elif args.command == 'make':
    exit('Not implemented yet')
else:
    exit('Unsupported command')
