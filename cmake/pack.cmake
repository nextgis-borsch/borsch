################################################################################
# Project:  CMake4GDAL
# Purpose:  CMake build scripts
# Author:   Dmitry Baryshnikov, polimax@mail.ru
################################################################################
# Copyright (C) 2024, NextGIS <info@nextgis.com>
# Copyright (C) 2024 Dmitry Baryshnikov
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
################################################################################

include(${CMAKE_CURRENT_LIST_DIR}/helper.cmake)

function(pack PACKAGE_NAME PACKAGE_VENDOR VERSION)
    if(REGISTER_PACKAGE)
        # Export the package for use from the build-tree
        # (this registers the build-tree with a global CMake-registry)
        string(TOUPPER ${PROJECT_NAME} PACKAGE_UPPER_NAME)
        export(PACKAGE ${PACKAGE_UPPER_NAME})
    endif()

    # Archiving ====================================================================

    set(CPACK_PACKAGE_NAME "${PACKAGE_NAME}")
    set(CPACK_PACKAGE_VENDOR "${PACKAGE_VENDOR}")
    set(CPACK_PACKAGE_VERSION "${VERSION}")
    set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PACKAGE_NAME} Installation")
    set(CPACK_PACKAGE_RELOCATABLE TRUE)
    set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
    set(CPACK_GENERATOR "ZIP")
    set(CPACK_MONOLITHIC_INSTALL ON)
    set(CPACK_STRIP_FILES TRUE)

    # Get cpack zip archive name
    get_cpack_filename(${VERSION} PROJECT_CPACK_FILENAME)
    set(CPACK_PACKAGE_FILE_NAME ${PROJECT_CPACK_FILENAME})
    include(CPack)
endfunction()

