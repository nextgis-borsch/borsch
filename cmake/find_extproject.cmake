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

function(get_imported_targets file_to_search targets)
    file(STRINGS ${file_to_search} targets_str
         REGEX "^foreach+([()_a-zA-Z0-9 ]+)")    
    string(SUBSTRING ${targets_str} 24 -1 targets_local)
    string(LENGTH ${targets_local} STR_LEN)
    math(EXPR LAST_INDEX "${STR_LEN} - 1")
    string(SUBSTRING ${targets_local} 0 ${LAST_INDEX} targets_local)  
    string(REPLACE " " ";" targets_local ${targets_local})
    set(${targets} ${targets_local} PARENT_SCOPE)
endfunction()

function(check_updates file_path update_period check)
    file(TIMESTAMP ${file_path} LAST_PULL "%y%j%H%M" UTC)
    if(NOT LAST_PULL)
        set(LAST_PULL 0)
    endif()
    string(TIMESTAMP CURRENT_TIME "%y%j%H%M" UTC)
    math(EXPR DIFF_TIME "${CURRENT_TIME} - ${LAST_PULL}")
    #message(STATUS "period ${update_period} diff ${DIFF_TIME} current ${CURRENT_TIME} last ${LAST_PULL}")
    if(DIFF_TIME GREATER ${update_period})
        set(${check} TRUE PARENT_SCOPE)
    else()
        set(${check} FALSE PARENT_SCOPE)
    endif()
endfunction()

function(color_message text)

    string(ASCII 27 Esc)
    set(BoldGreen   "${Esc}[1;32m")
    set(ColourReset "${Esc}[m")
        
    message(STATUS "${BoldGreen}${text}${ColourReset}")
    
endfunction() 

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
    
    if(NOT DEFINED PULL_UPDATE_PERIOD)
        set(PULL_UPDATE_PERIOD 5)
    endif()

    if(NOT DEFINED SUPRESS_WITH_MESSAGES)
        set(SUPRESS_WITH_MESSAGES TRUE)
    endif()

    list(APPEND find_extproject_CMAKE_ARGS -DEP_BASE=${EP_BASE})   
    list(APPEND find_extproject_CMAKE_ARGS -DEP_URL=${EP_URL})       
    list(APPEND find_extproject_CMAKE_ARGS -DPULL_UPDATE_PERIOD=${PULL_UPDATE_PERIOD})       
        
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
        if(NOT SUPRESS_WITH_MESSAGES)
            message(STATUS "${_variableName}=${${_variableName}}")
        endif()    
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
        color_message("Git clone ${repo_name} ...")
        execute_process(COMMAND ${GIT_EXECUTABLE} clone ${EP_URL}/${repo_name} ${name}_EP
           WORKING_DIRECTORY  ${EP_BASE}/Source)
   
    else() 
        check_updates(${EP_BASE}/Stamp/${name}_EP/${name}_EP-gitpull.txt ${PULL_UPDATE_PERIOD} CHECK_UPDATES)
        if(CHECK_UPDATES)
            color_message("Git pull ${repo_name} ...")
            execute_process(COMMAND ${GIT_EXECUTABLE} pull
               WORKING_DIRECTORY  ${EP_BASE}/Source/${name}_EP)
            file(WRITE ${EP_BASE}/Stamp/${name}_EP/${name}_EP-gitpull.txt "")    
        endif()        
    endif()
     
    execute_process(COMMAND ${CMAKE_COMMAND} ${EP_BASE}/Source/${name}_EP
       ${find_extproject_CMAKE_ARGS}
       WORKING_DIRECTORY ${EP_BASE}/Build/${name}_EP RESULT_VARIABLE _rv)
    
    if(${_rv} EQUAL 0) 
        string(TOUPPER ${name}_FOUND IS_FOUND)
        set(${IS_FOUND} TRUE PARENT_SCOPE)  
    endif()          
    
    include(${EP_BASE}/Build/${name}_EP/${repo_project}-exports.cmake) 
    get_imported_targets(${EP_BASE}/Build/${name}_EP/${repo_project}-exports.cmake IMPOTED_TARGETS)
    
    add_dependencies(${IMPOTED_TARGETS} ${name}_EP)  
    
    set(DEPENDENCY_LIB ${DEPENDENCY_LIB} ${IMPOTED_TARGETS} PARENT_SCOPE)   
    set(TARGET_LINK_LIB ${TARGET_LINK_LIB} ${IMPOTED_TARGETS} PARENT_SCOPE)
    
    include_directories(${EP_BASE}/Install/${name}_EP/include)
    foreach (inc ${repo_include})
        include_directories(${EP_BASE}/Install/${name}_EP/include/${inc})
    endforeach ()    
    
    install( DIRECTORY ${EP_BASE}/Install/${name}_EP/ DESTINATION ${CMAKE_INSTALL_PREFIX} )
    
endfunction()
