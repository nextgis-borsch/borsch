################################################################################
# Project:  external projects
# Purpose:  CMake build scripts
# Author:   Dmitry Baryshnikov, polimax@mail.ru
################################################################################
# Copyright (C) 2015, NextGIS <info@nextgis.com>
# Copyright (C) 2015, Dmitry Baryshnikov
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

set(TARGET_LINK_LIB) # ${TARGET_LINK_LIB} ""
set(DEPENDENCY_LIB) # ${DEPENDENCY_LIB} ""
set(WITHOPT ${WITHOPT} "")

function(find_anyproject name)

    include (CMakeParseArguments)
    set(options OPTIONAL REQUIRED QUIET EXACT MODULE)
    set(oneValueArgs DEFAULT VERSION)
    set(multiValueArgs CMAKE_ARGS COMPONENTS)
    cmake_parse_arguments(find_anyproject "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )  
    
    if (find_anyproject_REQUIRED OR find_anyproject_DEFAULT)
        set(_WITH_OPTION_ON TRUE)
    else()  
        set(_WITH_OPTION_ON FALSE)
    endif()
    
    set(WITHOPT "${WITHOPT}option(WITH_${name} \"Set ON to use ${name}\" ${_WITH_OPTION_ON})\n")
    set(WITHOPT "${WITHOPT}option(WITH_${name}_EXTERNAL \"Set ON to use external ${name}\" OFF)\n")

    option(WITH_${name} "Set ON to use ${name}" ${_WITH_OPTION_ON})

    if(WITH_${name})
        option(WITH_${name}_EXTERNAL "Set ON to use external ${name}" OFF)
        if(WITH_${name}_EXTERNAL)
            include(find_extproject)
            find_extproject(${name} ${ARGN})
        else()
            # transfer some input options to find_package arguments
            if(find_anyproject_VERSION)
                set(FIND_PROJECT_ARG ${find_anyproject_VERSION})
            endif()
            if(find_anyproject_EXACT)
                set(FIND_PROJECT_ARG ${FIND_PROJECT_ARG} EXACT)
            endif()
            if(find_anyproject_QUIET)
                set(FIND_PROJECT_ARG ${FIND_PROJECT_ARG} QUIET)
            endif()
            if(find_anyproject_MODULE)
                set(FIND_PROJECT_ARG ${FIND_PROJECT_ARG} MODULE)
            endif()
            if(find_anyproject_REQUIRED)
                set(FIND_PROJECT_ARG ${FIND_PROJECT_ARG} REQUIRED)
            endif()
            if(find_anyproject_COMPONENTS)
                set(FIND_PROJECT_ARG ${FIND_PROJECT_ARG} COMPONENTS ${find_anyproject_COMPONENTS})
            endif()
            
            find_package(${name} ${FIND_PROJECT_ARG})
        endif()
        
        if(${name}_FOUND) 
            set(${name}_FOUND TRUE CACHE BOOL "use ${name} external")  
            mark_as_advanced(${name}_FOUND)
        endif()
    endif()
    
    if(NOT WITH_${name}_EXTERNAL AND ${name}_FOUND)
        include_directories(${${name}_INCLUDE_DIRS})
        set(TARGET_LINK_LIB ${TARGET_LINK_LIB} ${${name}_LIBRARIES} PARENT_SCOPE)
    else()
        set(TARGET_LINK_LIB ${TARGET_LINK_LIB} PARENT_SCOPE)   
        set(DEPENDENCY_LIB ${DEPENDENCY_LIB} PARENT_SCOPE)    
    endif()
    set(WITHOPT ${WITHOPT} PARENT_SCOPE)
endfunction()

function(target_link_extlibraries name)
    if(DEPENDENCY_LIB)
        add_dependencies(${name} ${DEPENDENCY_LIB})  
    endif()    
    if(TARGET_LINK_LIB)
        list(REMOVE_DUPLICATES TARGET_LINK_LIB)
        target_link_libraries(${name} ${TARGET_LINK_LIB})
    endif()
    file(WRITE ${CMAKE_BINARY_DIR}/ext_options.cmake ${WITHOPT})
endfunction()

