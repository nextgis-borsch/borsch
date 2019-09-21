#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Purpose: Various tools
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
    {"url" : "googletest", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_boost", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_cgal", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ['-DBUILD_TESTING=OFF', '-DWITH_CPACK=OFF']},
    {"url" : "lib_xml2", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_z", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_openssl", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DOPENSSL_NO_DYNAMIC_ENGINE=ON']},
    {"url" : "lib_curl", "cmake_dir" : "CMake", "build" : ["mac", "win"], "args" : ['-DWITH_OpenSSL=ON', '-DWITH_ZLIB=ON', '-DENABLE_THREADED_RESOLVER=ON', '-DCMAKE_USE_GSSAPI=ON', '-DCMAKE_USE_LIBSSH2=OFF']},
    {"url" : "lib_ecw", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_expat", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DBUILD_tools=ON']},
    {"url" : "lib_iconv", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_gif", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_qhull", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_freexl", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_geojsonvt", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_geos", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_tiff", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DWITH_ZLIB=ON', '-DWITH_JPEG=ON', '-DWITH_JPEG12=ON', '-DWITH_JBIG=ON', '-DWITH_LibLZMA=ON']},
    {"url" : "lib_geotiff", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DWITH_ZLIB=ON', '-DWITH_JPEG=ON']},
    {"url" : "lib_jpeg", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_szip", "cmake_dir" : "cmake", "build" : ["mac"], "args" : ['-DBUILD_TESTS=OFF']},
    {"url" : "lib_hdf4", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DWITH_SZIP=ON']},
    {"url" : "lib_hdfeos2", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_jbig", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_jpegturbo", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_jsonc", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_lzma", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_mrsid", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_nunicode", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_opencad", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_png", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_pq", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_sqlite", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_proj", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_gsl", "cmake_dir" : "cmake", "build" : ["mac","win"], "args" : ['-DBUILD_TESTS=OFF']},
    {"url" : "lib_openjpeg", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_gdal", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DWITH_EXPAT=ON', '-DWITH_GeoTIFF=ON', '-DWITH_ICONV=ON', '-DWITH_JSONC=ON', '-DWITH_LibXml2=ON', '-DWITH_TIFF=ON', '-DWITH_ZLIB=ON', '-DWITH_JBIG=ON', '-DWITH_JPEG=ON', '-DWITH_JPEG12=ON', '-DWITH_LibLZMA=ON', '-DWITH_PYTHON=ON', '-DWITH_PYTHON3=OFF', '-DWITH_PNG=ON', '-DWITH_OpenSSL=ON', '-DENABLE_OZI=ON', '-DENABLE_NITF_RPFTOC_ECRGTOC=ON', '-DGDAL_ENABLE_GNM=ON', '-DWITH_SQLite3=ON', '-DWITH_PostgreSQL=ON', '-DGDAL_BUILD_APPS=ON', '-DENABLE_OPENJPEG=ON', '-DWITH_OpenJPEG=ON', '-DENABLE_HDF4=ON', '-DWITH_QHULL=ON']},
    {"url" : "lib_rapidjson", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_spatialindex", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DBUILD_TESTS=OFF']},
    {"url" : "lib_spatialite", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DOMIT_FREEXL=ON', '-DENABLE_LWGEOM=OFF', '-DGEOS_TRUNK=ON']},
    {"url" : "lib_qt4", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_qt5", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_qca", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DBUILD_TESTS=OFF', '-DQT4_BUILD=ON']},
    {"url" : "lib_qwt", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DQT4_BUILD=ON', '-DWITH_QWTMATHML=OFF', '-DWITH_QWTDESIGNER=OFF', '-DWITH_QWTPLAYGROUND=OFF', '-DWITH_QWTEXAMPLES=OFF']},
    {"url" : "lib_uv", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_variant", "cmake_dir" : "cmake", "build" : [], "args" : []},
    {"url" : "lib_zip", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "lib_yaml", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_freetype", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_opencv", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "lib_agg", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "python", "cmake_dir" : "cmake", "build" : ["win"], "args" : ["-DPYTHON_VERSION=2.7.12", "-DBUILD_LIBPYTHON_SHARED=ON"]},
    {"url" : "py_setuptools", "cmake_dir" : "cmake", "build" : ["win"], "args" : []},
    {"url" : "py_future", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_raven", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "py_contextlib", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "numpy", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_sip", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_qt4", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "lib_qscintilla", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : ['-DQT4_BUILD=ON', '-DWITH_BINDINGS=ON']},
    {"url" : "py_psycopg", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_dateutil", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_pygments", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_ows", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_httplib", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_yaml", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_jinja", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_markupsafe", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_nose", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_pytz", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_six", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_requests", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_spatialite", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_exifread", "cmake_dir" : "cmake", "build" : ["mac", "win"], "args" : []},
    {"url" : "py_matplotlib", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "py_parsing", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "py_cycler", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "py_subprocess32", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "py_functools_lru_cache", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "py_kiwisolver", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "postgis", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
    {"url" : "tests", "cmake_dir" : "cmake", "build" : [], "args" : []},
    # {"url" : "qgis", "cmake_dir" : "cmake", "build" : ["mac"], "args" : []},
]

args = {}
organize_file = 'folders.csv'
install_dir = 'inst'
max_os_min_version = '10.11'
mac_os_sdks_path = '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs'

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
    parser_make.add_argument('--generator', dest='generator_name', default=None, help='specify a build system generator')
    parser_make.add_argument('--only', dest='only_repos', default=None, help='the names of the packages separated by comma')
    parser_make.add_argument('--versions', dest='versions', action='store_true', help='print libraries version')
    parser_make.add_argument('--clean', dest='clean', action='store_true', default=False, help='clean packages')

    parser_organize = subparsers.add_parser('organize')
    parser_organize.add_argument('--src', dest='src', required=True, help='original sources folder')
    parser_organize.add_argument('--dst_name', dest='dst_name', required=True, help='destination folder name')
    parser_organize.add_argument('--dst_path', dest='dst_path', required=False, help='Specify destination folder path')

    parser_install_all = subparsers.add_parser('install_all')
    parser_install_all.add_argument(dest='install_dst', default=None, help='the names of the packages separated by comma')

    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('--script', dest='script', required=True, help='the name of updated script')

    args = parser.parse_args()

def run(args):
    # print 'calling ' + string.join(args)
    try:
        if args[0] == "git":
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            if 'nothing to commit' in output or 'Already up-to-date' in output or 'Everything up-to-date' in output:
                return True
            else:
                print output
                return True
        else:
            output_code = subprocess.call(args, stderr=subprocess.STDOUT)
            return output_code == 0
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
        color_print('clone ' + repository['url'], True, 'LCYAN')
        if sys.platform == 'win32':
            run(('git', 'clone', '--depth', '1', 'https://github.com/nextgis-borsch/' + repository['url'] + '.git'))
        else:
            run(('git', 'clone', '--depth', '1', 'git@github.com:nextgis-borsch/' + repository['url'] + '.git'))

def git_status():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        color_print('status ' + repository['url'], True, 'LGREEN')
        try:
            os.chdir(repository['url'])
            run(('git', 'status'))
            os.chdir(os.path.join(os.getcwd(), os.pardir))
        except:
            pass

def git_pull():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        color_print('pull ' + repository['url'], True, 'LYELLOW')
        try:
            os.chdir(repository['url'])
            run(('git', 'pull'))
            os.chdir(os.path.join(os.getcwd(), os.pardir))
        except:
            pass

def git_push():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        color_print('push ' + repository['url'], True, 'LCYAN')
        try:
            os.chdir(repository['url'])
            run(('git', 'push'))
            os.chdir(os.path.join(os.getcwd(), os.pardir))
        except:
            pass

def git_commit(message):
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    for repository in repositories:
        color_print('commit to ' + repository['url'] + ' with message: ' + message, True, 'LCYAN')
        try:
            os.chdir(repository['url'])
            if run(('git', 'commit', '-a', '-m', message)):
                color_print('All is OK', True, 'LMAGENTA')
            os.chdir(os.path.join(os.getcwd(), os.pardir))
        except:
            pass

def make_versions():
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    root_dir = os.getcwd()
    for repository in repositories:
        repo_build_dir = os.path.join(root_dir, repository['url'], 'build')
        version_file_path = os.path.join(repo_build_dir, 'version.str')
        if not os.path.exists(version_file_path):
            color_print(repository['url'] + ' - unknown', False, 'LRED')
        else:
            with open(version_file_path) as f:
                content = f.readlines()
                version_str = content[0].rstrip()
                color_print(repository['url'] + ' - ' + version_str, False, 'LGREEN')

def update_scripts(script):
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    repo_root = os.getcwd()
    script_path = os.path.join(repo_root, 'borsch', 'cmake', script)

    for repository in repositories:
        color_print('update ' + repository['url'], False, 'LYELLOW')
        if repository['url'] == 'borsch':
            continue
        repo_cmake_path = os.path.join(repo_root, repository['url'], repository['cmake_dir'], script)
        if os.path.exists(repo_cmake_path):
            shutil.copyfile(script_path, repo_cmake_path)
            color_print('OK', True, 'LCYAN')


def make_package(repositories, generator):
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    repo_root = os.getcwd()

    for repository in repositories:
        run_args = ['cmake']
        check_os = ''
        run_args.append('-DSUPPRESS_VERBOSE_OUTPUT=ON')
        run_args.append('-DCMAKE_BUILD_TYPE=Release')
        run_args.append('-DSKIP_DEFAULTS=ON')
        build_args = ''
        if sys.platform == 'darwin':
            check_os = 'mac'
            run_args.append('-DOSX_FRAMEWORK=ON')
            run_args.append('-DREGISTER_PACKAGE=ON')
            run_args.append('-DCMAKE_OSX_SYSROOT=' + mac_os_sdks_path + '/MacOSX.sdk')
            run_args.append('-DCMAKE_OSX_DEPLOYMENT_TARGET=' + max_os_min_version)
            build_args = '-j' + str(multiprocessing.cpu_count())
        elif sys.platform == 'win32':
            if generator is not None:
                run_args.append('-G')
                run_args.append(generator)
            run_args.append('-DREGISTER_PACKAGE=ON')
            run_args.append('-DBUILD_SHARED_LIBS=TRUE')
            check_os = 'win'
            build_args = '/m:' + str(multiprocessing.cpu_count())
        else:
            check_os = 'nix'

        if check_os in repository['build']:
            color_print('make ' + repository['url'], True, 'LRED')
            repo_dir = os.path.join(repo_root, repository['url'])
            repo_build_dir = os.path.join(repo_dir, 'build')
            repo_inst_dir = os.path.join(repo_dir, install_dir)
            run_args.append('-DCMAKE_INSTALL_PREFIX=' + repo_inst_dir)
            if not os.path.exists(repo_build_dir):
                os.makedirs(repo_build_dir)
            if not os.path.exists(repo_inst_dir):
                os.makedirs(repo_inst_dir)
            os.chdir(repo_build_dir)
            for repo_build_arg in repository['args']:
                run_args.append(repo_build_arg)
            run_args.append('..')
            color_print('configure ' + repository['url'], False, 'LBLUE')
            if run((run_args)):
                color_print('build ' + repository['url'], False, 'LBLUE')
                if run(('cmake', '--build', '.', '--config', 'release', '--', build_args)):
                    color_print('install ' + repository['url'], False, 'LBLUE')
                    run(('cmake', '--build', '.', '--config', 'release', '--target', 'install'))
                else:
                    sys.exit("Build %s error!" % repository['url'])
            else:
                sys.exit("Configure %s error!" % repository['url'])
            # Special case to build JPEG12 package
            if  repository['url'] == 'lib_jpeg':
                color_print('Special case for ' + repository['url'] + '12', False, 'LBLUE')
                color_print('make ' + repository['url'] + '12', True, 'LRED')
                repo_build_dir = os.path.join(repo_dir, 'build12')
                if not os.path.exists(repo_build_dir):
                    os.makedirs(repo_build_dir)
                run_args.insert(4, '-DBUILD_JPEG_12=ON')
                if not os.path.exists(repo_build_dir):
                    os.makedirs(repo_build_dir)
                os.chdir(repo_build_dir)
                if run((run_args)):
                    if run(('cmake', '--build', '.', '--config', 'release', '--', build_args)):
                        run(('cmake', '--build', '.', '--config', 'release', '--target', 'install'))

        os.chdir(repo_root)

def clean_all(repositories):
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    repo_root = os.getcwd()

    for repository in repositories:
        check_os = ''
        if sys.platform == 'darwin':
            check_os = 'mac'
        elif sys.platform == 'win32':
            check_os = 'win'
        else:
            check_os = 'nix'

        if check_os in repository['build']:
            color_print('remove build for ' + repository['url'], True, 'LRED')
            repo_dir = os.path.join(repo_root, repository['url'])
            repo_build_dir = os.path.join(repo_dir, 'build')

            shutil.rmtree(repo_build_dir)

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
            if '*' in exts or file_name in exts: # Check file name or if * mask
                shutil.copy(f, dest)
            else:
                file_extension = os.path.splitext(f)[1].replace('.','') # Check extension
                if file_extension != '' and file_extension in exts:
                    shutil.copy(f, dest)

def organize_sources(dst_name, dst_path=None):
    if dst_path is None:
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

        # Process name with [a-c]
        append_values = []
        for i, val in enumerate(exts):
            beg = val.find('[')
            end = val.find(']')
            if beg != -1 and end != -1:
                name_range = val[beg + 1:end]
                range_values = name_range.split('-')
                for i in range(int(range_values[0]), int(range_values[1])):
                    append_values.append(val[:beg] + str(i) + val[end + 1:])

        exts.extend(append_values)

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

    postprocess_path =  os.path.join(dst_path, 'opt', 'postprocess.py')
    if os.path.exists(postprocess_path):
        os.chdir(os.path.join(dst_path, 'opt'))
        run(('python', 'postprocess.py', sources_dir))

def install_all(install_dst):
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))
    repo_root = os.getcwd()

    if not os.path.exists(install_dst):
        os.mkdir(install_dst)

    def copytree(src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    try:
                        shutil.copy2(s, d)
                    except:
                        print "Error with copy ", s

    for f in os.listdir('.'):
        for_copy = os.path.join(repo_root, f, "inst")
        print "Copy %s" % for_copy
        if os.path.exists(for_copy):
            copytree(for_copy, install_dst)

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
    if args.versions:
        make_versions()
        exit(0)
    if args.only_repos is not None:
        repositories = [repo for repo in repositories if repo['url'] in args.only_repos.split(',')]

    if not args.clean:
        make_package(repositories, args.generator_name)
    else:
        clean_all(repositories)
elif args.command == 'organize':
    organize_sources(args.dst_name, args.dst_path)
elif args.command == 'install_all':
    install_all(args.install_dst)
elif args.command == 'update':
    update_scripts(args.script)
else:
    exit('Unsupported command')
