#.rst:
# FindJBIG
# ---------
#
# Find jbig kit
#
#   JBIG_INCLUDE_DIRS - where to find jbig.h, etc.
#   JBIG_LIBRARIES    - List of libraries when using jbig.
#   JBIG_FOUND        - True if jbig kit found.

#=============================================================================
# Copyright 2015, NextGIS <info@nextgis.com>
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
include(${CMAKE_CURRENT_LIST_DIR}/FindPackageHandleStandardArgs.cmake)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(JBIG
                                  REQUIRED_VARS JBIG_LIBRARY JBIG_INCLUDE_DIR
                                  VERSION_VAR JBIG_VERSION_STRING)

# Copy the results to the output variables.
if(JBIG_FOUND)
  set(JBIG_LIBRARIES ${JBIG_LIBRARY})
  set(JBIG_INCLUDE_DIRS ${JBIG_INCLUDE_DIR})
endif()

mark_as_advanced(JBIG_INCLUDE_DIR JBIG_LIBRARY)
