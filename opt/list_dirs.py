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
rootdir = os.getcwd()
queue = [rootdir]
lst = []
while queue:
    file = queue.pop(0)
    if os.path.isdir(file):
        lst.append(file)
        queue.extend(os.path.join(file,x) for x in os.listdir(file))

lst = sorted(lst)
for path in lst:
    print path
