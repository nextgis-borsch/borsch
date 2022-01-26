#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Purpose: Script to listt all directories in cwd
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Copyright (c) 2018 NextGIS <info@nextgis.com>
## License: GPL v.2
##
################################################################################

import os
import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List subdirectories')
    parser.add_argument('--in_path', help='root directory path', required=True)
    parser.add_argument('--out_path', help='output csv file path', required=True)
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    rootdir = args.in_path
    queue = [rootdir]
    lst = []
    while queue:
        file = queue.pop(0)
        if os.path.isdir(file):
            # Skip root path
            file_in = file.replace(rootdir, '')
            if file_in.startswith('/'):
                file_in = file_in[1:]
            lst.append(file_in)
            queue.extend(os.path.join(file,x) for x in os.listdir(file))

    lst = sorted(lst)
    with open(args.out_path, 'w') as csvfile:
        fieldnames = ['in_path', 'out_path', 'skip', 'ext']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for path in lst:
            writer.writerow({'in_path': path, 'out_path': path, 'skip': 'skip', 'ext': '*'})
            # print(path)
