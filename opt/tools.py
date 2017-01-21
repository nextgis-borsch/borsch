#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Author: Maxim Dubinin <maim.dubinin@nextgis.com>
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
import multiprocessing
import glob
import csv

repositories = [
    {"url" : "borsch", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_z", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_jsonc", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_iconv", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_geos", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_proj", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_openssl", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ['-DOPENSSL_NO_DYNAMIC_ENGINE=ON']},
    {"url" : "lib_szip", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_jpeg", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_jbig", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_expat", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_zip", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_curl", "cmake_dir" : "CMake", "build" : ["mac"], "args" : ['-DWITH_OpenSSL=ON', '-DWITH_ZLIB=ON', '-DENABLE_THREADED_RESOLVER=ON', '-DCMAKE_USE_GSSAPI=ON', '-DCMAKE_USE_LIBSSH2=OFF']},
    {"url" : "lib_png", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_lzma", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_tiff", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ['-DWITH_ZLIB=ON', '-DWITH_JPEG=ON', '-DWITH_JPEG12=ON', '-DWITH_JBIG=ON', '-DWITH_LibLZMA=ON']},
    {"url" : "lib_hdf4", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_geotiff", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ['-DWITH_ZLIB=ON', '-DWITH_JPEG=ON']},
    {"url" : "lib_pq", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "tests", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_xml2", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_sqlite", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_hdfeos2", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_gdal", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ['-DWITH_EXPAT=ON', '-DWITH_GeoTIFF=ON', '-DWITH_ICONV=ON', '-DWITH_JSONC=ON', '-DWITH_LibXml2=ON', '-DWITH_TIFF=ON', '-DWITH_ZLIB=ON', '-DWITH_JBIG=ON', '-DWITH_JPEG=ON', '-DWITH_JPEG12=ON', '-DWITH_LibLZMA=ON', '-DWITH_PYTHON=ON', '-DWITH_PYTHON3=OFF', '-DWITH_PNG=ON', '-DWITH_OpenSSL=ON', '-DENABLE_OZI=ON', '-DENABLE_NITF_RPFTOC_ECRGTOC=ON', '-DGDAL_ENABLE_GNM=ON', '-DWITH_SQLite3=ON', '-DWITH_PostgreSQL=ON']},
    {"url" : "lib_spatialite", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_freexl", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_spatialindex", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_qt4", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "postgis", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "googletest", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_boost", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_uv", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_jpegturbo", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_variant", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_rapidjson", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_nunicode", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_geojsonvt", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_opencad", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_ecw", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_mrsid", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "numpy", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
]

args = {}
organize_file = 'folders.csv'

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

#print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC

def parse_arguments():
    global args

    parser = argparse.ArgumentParser(description='NextGIS Borsch tools.')
    parser.add_argument('-v', '--version', action='version', version='NextGIS Borsch tools version 1.0')

    subparsers = parser.add_subparsers(help='command help', dest='command')
    parser_git = subparsers.add_parser('git')
    parser_git.add_argument('--clone', dest='clone', action='store_true', help='clone all repositories')
    parser_git.add_argument('--pull', dest='pull', action='store_true', help='update all repositories')
    parser_git.add_argument('--status', dest='status', action='store_true', help='print status of repositories')
    parser_git.add_argument('--push', dest='push', action='store_true', help='send changes to server')
    parser_git.add_argument('--commit', dest='message', help='commit changes in repositories')

    parser_make = subparsers.add_parser('make')

    parser_organize = subparsers.add_parser('organize')
    parser_organize.add_argument('--src', dest='src', required=True, help='original sources folder')
    parser_organize.add_argument('--dst_name', dest='dst_name', required=True, choices=['qgis', 'lib_gdal'], help='destination folder name')

    args = parser.parse_args()

def run(args):
    print 'calling ' + string.join(args)
    try:
        subprocess.check_call(args)
        return True
    except subprocess.CalledProcessError, e:
        return False

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

def git_clone():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        print color_print('clone ' + repository['url'], True, 'LCYAN')
        run(('git', 'clone', '--depth', '1', 'git@github.com:nextgis-borsch/' + repository['url'] + '.git'))

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
        if run(('git', 'pull')):
            color_print('All is OK', True, 'LMAGENTA')
        os.chdir(os.path.join(os.getcwd(), os.pardir))

def git_push():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        print color_print('push ' + repository['url'], True, 'LCYAN')
        os.chdir(repository['url'])
        if run(('git', 'push')):
            color_print('All is OK', True, 'LMAGENTA')
        os.chdir(os.path.join(os.getcwd(), os.pardir))

def git_commit(message):
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        print color_print('commit to ' + repository['url'] + ' with message: ' + message, True, 'LCYAN')
        os.chdir(repository['url'])
        if run(('git', 'commit', '-a', '-m', message)):
            color_print('All is OK', True, 'LMAGENTA')
        os.chdir(os.path.join(os.getcwd(), os.pardir))

def make_package():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    repo_root = os.getcwd()
    for repository in repositories:
        run_args = ['cmake']
        check_os = ''
        run_args.append('-DSUPPRESS_VERBOSE_OUTPUT=ON')
        build_args = ''
        if sys.platform == 'darwin':
            check_os = 'mac'
            run_args.append('-DOSX_FRAMEWORK=ON')
            run_args.append('-DREGISTER_PACKAGE=ON')
            build_args = '-j' + str(multiprocessing.cpu_count())
        elif sys.platform == 'win32':
            check_os = 'win'
        else:
            check_os = 'nix'

        if check_os in repository['build']:
            print color_print('make ' + repository['url'], True, 'LRED')
            repo_dir = os.path.join(repo_root, repository['url'])
            repo_build_dir = os.path.join(repo_dir, 'build')
            repo_inst_dir = os.path.join(repo_dir, 'inst')
            run_args.append('-DCMAKE_INSTALL_PREFIX=' + repo_inst_dir)
            if not os.path.exists(repo_build_dir):
                os.makedirs(repo_build_dir)
            if not os.path.exists(repo_inst_dir):
                os.makedirs(repo_inst_dir)
            os.chdir(repo_build_dir)
            for repo_build_arg in repository['args']:
                run_args.append(repo_build_arg)
            run_args.append('..')
            print color_print('configure ' + repository['url'], False, 'LBLUE')
            if run((run_args)):
                print color_print('build ' + repository['url'], False, 'LBLUE')
                if run(('cmake', '--build', '.', '--config', 'release', '--', build_args)):
                    print color_print('install ' + repository['url'], False, 'LBLUE')
                    run(('cmake', '--build', '.', '--config', 'release', '--target', 'install'))

            # Special case to build JPEG12 package
            if  repository['url'] == 'lib_jpeg':
                print color_print('Special case for ' + repository['url'] + '12', False, 'LBLUE')
                print color_print('make ' + repository['url'] + '12', True, 'LRED')
                repo_build_dir = os.path.join(repo_dir, 'build12')
                if not os.path.exists(repo_build_dir):
                    os.makedirs(repo_build_dir)
                run_args.insert(5, '-DBUILD_JPEG_12=ON')
                if not os.path.exists(repo_build_dir):
                    os.makedirs(repo_build_dir)
                os.chdir(repo_build_dir)
                if run((run_args)):
                    if run(('cmake', '--build', '.', '--config', 'release', '--', build_args)):
                        run(('cmake', '--build', '.', '--config', 'release', '--target', 'install'))

        os.chdir(repo_root)

def read_mappings(csv_path):
    fieldnames_data = ('old','new','action','ext2keep')
    f_csv = open(csv_path)
    csvreader = csv.DictReader(f_csv, fieldnames=fieldnames_data)

    return csvreader

def copy_dir(src, dest, exts):
    if not os.path.exists(dest):
        os.makedirs(dest)

    files = glob.glob(src + "/*")
    for f in files:
        if not os.path.isdir(f):
            file_name = os.path.basename(f)
            if file_name in exts:
                shutil.copy(f, dest)
            else:
                file_extension = os.path.splitext(f)[1].replace('.','')
                if file_extension != '' and file_extension in exts:
                    shutil.copy(f, dest)

def organize_sources(dst_name):
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    repo_root = os.getcwd()
    dst_path = os.path.join(repo_root, dst_name)
    if not os.path.exists(dst_path):
        exit('Destination path ' + dst_path + ' not exists')
    organize_file_path = os.path.join(dst_path, 'opt', organize_file)
    if not os.path.exists(organize_file_path):
        exit('Organize file ' + organize_file_path + ' not exists')

    sources_dir = args.src
    if not os.path.exists(sources_dir):
        exit('Source path ' + sources_dir + ' not exists')

    mappings = read_mappings(organize_file_path)

    for row in mappings:
        action = row['action']
        exts = row['ext2keep']
        if exts is not None:
            exts = exts.split(',')

        if row['old'] is None or row['old'] == '':
            from_folder = sources_dir
        else:
            from_folder = os.path.join(sources_dir, row['old'])

        if row['new'] is None or row['new'] == '':
            to_folder = dst_path
        else:
            to_folder = os.path.join(dst_path, row['new'])

        if os.path.exists(from_folder):
            if action == 'skip':
                color_print(from_folder + ' ... skip', False, 'LBLUE' )
                continue
            else:
                copy_dir(from_folder, to_folder, exts)
                color_print(from_folder + ' ... processed', False, 'LYELLOW' )


parse_arguments()
if args.command == 'git':
    if args.status:
        git_status()
    if args.pull:
        git_pull()
    if args.push:
        git_push()
    if args.clone:
        git_clone()
    if args.message is not None and args.message != '':
        git_commit(args.message)
elif args.command == 'make':
    make_package()
elif args.command == 'organize':
    organize_sources(args.dst_name)
else:
    exit('Unsupported command')
