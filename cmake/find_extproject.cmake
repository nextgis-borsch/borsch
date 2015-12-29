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

function(find_extproject name)
  
    include (CMakeParseArguments)
  
    set(options OPTIONAL)
    set(oneValueArgs )
    set(multiValueArgs CMAKE_ARGS)
    cmake_parse_arguments(find_extproject "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )
    
    # set default third party lib path
    if(NOT DEFINED EP_BASE)
        set(EP_BASE "${CMAKE_BINARY_DIR}/third-party")
    endif()

    # set default url
    if(NOT DEFINED EP_URL)
        set(EP_URL "https://github.com/nextgis-extra")
    endif()  

    list(APPEND find_extproject_CMAKE_ARGS -DEP_BASE=${EP_BASE})   
    list(APPEND find_extproject_CMAKE_ARGS -DEP_URL=${EP_URL})       
        
    include(ExternalProject)
    set_property(DIRECTORY PROPERTY "EP_BASE" ${EP_BASE})

    
    # search CMAKE_INSTALL_PREFIX
    string (REGEX MATCHALL "(^|;)-DCMAKE_INSTALL_PREFIX[A-Za-z0-9_]*" _matchedVars "${find_extproject_CMAKE_ARGS}")    
    list(LENGTH _matchedVars _list_size)    
    if(_list_size EQUAL 0)
        list(APPEND find_extproject_CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${EP_BASE}/Install/${name}_EP)
    endif()
    
    # search CMAKE_INSTALL_PREFIX
    string (REGEX MATCHALL "(^|;)-DBUILD_SHARED_LIBS[A-Za-z0-9_]*" _matchedVars "${find_extproject_CMAKE_ARGS}")   
    unset(_matchedVars)
    list(LENGTH _matchedVars _list_size)    
    if(_list_size EQUAL 0)
        list(APPEND find_extproject_CMAKE_ARGS -DBUILD_SHARED_LIBS=${BUILD_SHARED_LIBS})
    endif()
    
    if(EXISTS ${EP_BASE}/Build/${name}_EP/ext_options.cmake)         
        include(${EP_BASE}/Build/${name}_EP/ext_options.cmake)
        # add include into  ext_options.cmake
        set(WITHOPT "${WITHOPT}include(${EP_BASE}/Build/${name}_EP/ext_options.cmake)\n" PARENT_SCOPE)    
    endif()
    
    get_cmake_property(_variableNames VARIABLES)
    string (REGEX MATCHALL "(^|;)WITH_[A-Za-z0-9_]*" _matchedVars "${_variableNames}") 
    foreach(_variableName ${_matchedVars})
        message(STATUS "${_variableName}=${${_variableName}}")
        list(APPEND find_extproject_CMAKE_ARGS -D${_variableName}=${${_variableName}})
    endforeach()
    
        
    # get some properties from <cmakemodules>/findext${name}.cmake file
    include(FindExt${name})
  
    ExternalProject_Add(${name}_EP
        GIT_REPOSITORY ${EP_URL}/${repo_name}
        CMAKE_ARGS ${find_extproject_CMAKE_ARGS}
    )
        
    find_package(Git)
    if(NOT GIT_FOUND)
      message(FATAL_ERROR "git is required")
      return()
    endif()
   
    if(NOT EXISTS "${EP_BASE}/Source/${name}_EP/.git")
        execute_process(COMMAND ${GIT_EXECUTABLE} clone ${EP_URL}/${repo_name} ${name}_EP
           WORKING_DIRECTORY  ${EP_BASE}/Source)
   
    else()    
        execute_process(COMMAND ${GIT_EXECUTABLE} pull
           WORKING_DIRECTORY  ${EP_BASE}/Source/${name}_EP)    
    endif()
     
    execute_process(COMMAND ${CMAKE_COMMAND} ${EP_BASE}/Source/${name}_EP
       ${find_extproject_CMAKE_ARGS}
       WORKING_DIRECTORY ${EP_BASE}/Build/${name}_EP RESULT_VARIABLE _rv)
    
    if(${_rv} EQUAL 0) 
        set(${name}_FOUND TRUE PARENT_SCOPE)  
    endif()          
    
    include(${EP_BASE}/Build/${name}_EP/${repo_project}-exports.cmake)  

    add_dependencies(${repo_project} ${name}_EP)  
    
    set(DEPENDENCY_LIB ${DEPENDENCY_LIB} ${repo_project} PARENT_SCOPE)   
    set(TARGET_LINK_LIB ${TARGET_LINK_LIB} ${repo_project} PARENT_SCOPE)
    
    include_directories(${EP_BASE}/Install/${name}_EP/include)
    foreach (inc ${repo_include})
        include_directories(${EP_BASE}/Install/${name}_EP/include/${inc})
    endforeach ()    
    
    install( DIRECTORY ${EP_BASE}/Install/${name}_EP/ DESTINATION ${CMAKE_INSTALL_PREFIX} )
    
endfunction()
