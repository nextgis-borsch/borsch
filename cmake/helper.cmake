################################################################################
# Project:  CMake4GDAL
# Purpose:  CMake build scripts
# Author:   Dmitry Baryshnikov, polimax@mail.ru
################################################################################
# Copyright (C) 2015-2024, NextGIS <info@nextgis.com>
# Copyright (C) 2012-2024 Dmitry Baryshnikov
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

# search python module
function(find_python_module module)
    string(TOUPPER ${module} module_upper)
    if(ARGC GREATER 1 AND ARGV1 STREQUAL "REQUIRED")
        set(${module}_FIND_REQUIRED TRUE)
    else()
        if (ARGV1 STREQUAL "QUIET")
            set(PY_${module}_FIND_QUIETLY TRUE)
        endif()
    endif()

    if(NOT PY_${module_upper})
        # A module's location is usually a directory, but for binary modules
        # it's a .so file.
        execute_process(COMMAND "${PYTHON_EXECUTABLE}" "-c"
            "import re, ${module}; print(re.compile('/__init__.py.*').sub('',${module}.__file__))"
            RESULT_VARIABLE _${module}_status
            OUTPUT_VARIABLE _${module}_location
            ERROR_QUIET
            OUTPUT_STRIP_TRAILING_WHITESPACE)
        if(NOT _${module}_status)
            set(PY_${module_upper} ${_${module}_location} CACHE STRING
                "Location of Python module ${module}")
        endif(NOT _${module}_status)
    endif(NOT PY_${module_upper})
    find_package_handle_standard_args(PY_${module} DEFAULT_MSG PY_${module_upper})
endfunction(find_python_module)

function(set_libraries libs is_shared bld_dir release_name debug_name)
    if (MSVC)
        if(is_shared)
            set(${libs}
                    debug "${bld_dir}/Debug/${CMAKE_SHARED_LIBRARY_PREFIX}${debug_name}${CMAKE_STATIC_LIBRARY_SUFFIX}"
                    optimized "${bld_dir}/Release/${CMAKE_SHARED_LIBRARY_PREFIX}${release_name}${CMAKE_STATIC_LIBRARY_SUFFIX}"
                PARENT_SCOPE)
        else()
            set(${libs}
                    debug"${bld_dir}/Debug/${CMAKE_STATIC_LIBRARY_PREFIX}${debug_name}${CMAKE_STATIC_LIBRARY_SUFFIX}"
                    optimized "${bld_dir}/Release/${CMAKE_STATIC_LIBRARY_PREFIX}${release_name}${CMAKE_STATIC_LIBRARY_SUFFIX}"
                PARENT_SCOPE)
        endif()
    else()
        if(is_shared)
            set(${libs}
                "${bld_dir}/${CMAKE_SHARED_LIBRARY_PREFIX}${debug_name}${CMAKE_SHARED_LIBRARY_SUFFIX}"
            PARENT_SCOPE)
        else()
            set(${libs}
                "${bld_dir}/${CMAKE_STATIC_LIBRARY_PREFIX}${release_name}${CMAKE_STATIC_LIBRARY_SUFFIX}"
            PARENT_SCOPE)
        endif()
    endif()
endfunction()

function(warning_msg text)
    if(NOT SUPPRESS_VERBOSE_OUTPUT)
    string(ASCII 27 Esc)
    set(Red         "${Esc}[31m")
    set(ColourReset "${Esc}[m")

    message(STATUS "${Red}${text}${ColourReset}")
    endif()
endfunction()

# macro to find packages on the host OS
macro(find_exthost_package)
    if(CMAKE_CROSSCOMPILING)
        set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER )
        set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY NEVER )
        set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE NEVER )

        find_package( ${ARGN} )

        set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM ONLY )
        set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY )
        set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY )
    else()
        find_package( ${ARGN} )
    endif()
endmacro()


# macro to find programs on the host OS
macro(find_exthost_program)
    if(CMAKE_CROSSCOMPILING)
        set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER )
        set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY NEVER )
        set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE NEVER )

        find_program( ${ARGN} )

        set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM ONLY )
        set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY )
        set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY )
    else()
        find_program( ${ARGN} )
    endif()
endmacro()

macro( find_exthost_path )
    if(CMAKE_CROSSCOMPILING)
        set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER )
        set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY NEVER )
        set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE NEVER )

        find_path( ${ARGN} )

        set( CMAKE_FIND_ROOT_PATH_MODE_PROGRAM ONLY )
        set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY )
        set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY )
    else()
        find_path( ${ARGN} )
    endif()
endmacro()


function(get_prefix prefix IS_STATIC)
  if(IS_STATIC)
    set(STATIC_PREFIX "static-")
      if(ANDROID)
        set(STATIC_PREFIX "${STATIC_PREFIX}android-${ANDROID_ABI}-")
      elseif(IOS)
        set(STATIC_PREFIX "${STATIC_PREFIX}ios-${IOS_ARCH}-")
      endif()
    endif()
  set(${prefix} ${STATIC_PREFIX} PARENT_SCOPE)
endfunction()


function(get_cpack_filename ver name)
    get_compiler_version(COMPILER)
    
    if(NOT DEFINED BUILD_STATIC_LIBS)
      set(BUILD_STATIC_LIBS OFF)
    endif()

    get_prefix(STATIC_PREFIX ${BUILD_STATIC_LIBS})

    set(${name} ${PROJECT_NAME}-${ver}-${STATIC_PREFIX}${COMPILER} PARENT_SCOPE)
endfunction()

function(get_compiler_version ver)
	if (CMAKE_C_COMPILER_ID)
		set(COMPILER_ID ${CMAKE_C_COMPILER_ID})
		set(COMPILER_VERSION ${CMAKE_C_COMPILER_VERSION})
	elseif(CMAKE_CXX_COMPILER_ID)
		set(COMPILER_ID ${CMAKE_CXX_COMPILER_ID})
		set(COMPILER_VERSION ${CMAKE_CXX_COMPILER_VERSION})
	else()
		message(FATAL_ERROR "No suitable compiler set. Please ensure you have a C or C++ compiler installed.")
	endif()

    ## Limit compiler version to 2 or 1 digits
    string(REPLACE "." ";" VERSION_LIST ${COMPILER_VERSION})
    list(LENGTH VERSION_LIST VERSION_LIST_LEN)
    if(VERSION_LIST_LEN GREATER 2 OR VERSION_LIST_LEN EQUAL 2)
        list(GET VERSION_LIST 0 COMPILER_VERSION_MAJOR)
        list(GET VERSION_LIST 1 COMPILER_VERSION_MINOR)
        set(COMPILER ${COMPILER_ID}-${COMPILER_VERSION_MAJOR}.${COMPILER_VERSION_MINOR})
    else()
        set(COMPILER ${COMPILER_ID}-${COMPILER_VERSION})
    endif()

    if(WIN32)
        if(CMAKE_CL_64)
            set(COMPILER "${COMPILER}-64bit")
        endif()
    endif()
    
    # Debug
    # set(COMPILER Clang-10.0)

    set(${ver} ${COMPILER} PARENT_SCOPE)
endfunction()
