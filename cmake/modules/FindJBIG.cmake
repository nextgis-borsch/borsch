#.rst:
# FindJBIG
# ---------
#
# Find jbig kit
#
#   JBIG_INCLUDE_DIRS - where to find jbig.h, etc.
#   JBIG_LIBRARIES    - List of libraries when using jbig.
#   JBIG_FOUND        - True if jbig kit found.
#
################################################################################
# Project:  external projects
# Purpose:  CMake build scripts
# Author:   Dmitry Baryshnikov, polimax@mail.ru
################################################################################
# Copyright (C) 2015, NextGIS <info@nextgis.com>
# Copyright (C) 2015 Dmitry Baryshnikov
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this script.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

# Look for the header file.
find_path(JBIG_INCLUDE_DIR NAMES jbig.h)

# Look for the library.
find_library(JBIG_LIBRARY NAMES jbig libjbig)

if (JBIG_INCLUDE_DIR AND EXISTS "${JBIG_INCLUDE_DIR}/jbig.h")
    file(STRINGS "${JBIG_INCLUDE_DIR}/jbig.h" jbig_version_str
         REGEX "^#[\t ]*define[\t ]+JBG_VERSION_(MAJOR|MINOR)[\t ]+[0-9]+$")

    unset(JBIG_VERSION_STRING)
    foreach(VPART MAJOR MINOR)
        foreach(VLINE ${jbig_version_str})
            if(VLINE MATCHES "^#[\t ]*define[\t ]+JBG_VERSION_${VPART}[\t ]+([0-9]+)$")
                set(JBIG_VERSION_PART "${CMAKE_MATCH_1}")
                if(JBIG_VERSION_STRING)
                    set(JBIG_VERSION_STRING "${JBIG_VERSION_STRING}.${JBIG_VERSION_PART}")
                else()
                    set(JBIG_VERSION_STRING "${JBIG_VERSION_PART}")
                endif()
            endif()
        endforeach()
    endforeach()
endif ()

# handle the QUIETLY and REQUIRED arguments and set JBIG_FOUND to TRUE if
# all listed variables are TRUE
include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(JBIG
                                  REQUIRED_VARS JBIG_LIBRARY JBIG_INCLUDE_DIR
                                  VERSION_VAR JBIG_VERSION_STRING)

# Copy the results to the output variables.
if(JBIG_FOUND)
  set(JBIG_LIBRARIES ${JBIG_LIBRARY})
  set(JBIG_INCLUDE_DIRS ${JBIG_INCLUDE_DIR})
endif()

mark_as_advanced(JBIG_INCLUDE_DIR JBIG_LIBRARY)
