################################################################################
# Project:  external projects
# Purpose:  CMake build scripts
# Author:   Dmitry Baryshnikov, dmitry.baryshnikov@nextgis.com
################################################################################
# Copyright (C) 2024, NextGIS <info@nextgis.com>
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

if(NOT DEFINED PACKAGE_VENDOR)
    set(PACKAGE_VENDOR NextGIS CACHE INTERNAL "Package vendor")
endif()

if(NOT DEFINED PACKAGE_BUGREPORT)
    set(PACKAGE_BUGREPORT info@nextgis.com CACHE INTERNAL "Package bugreport")
endif()

set(BUILD_TARGET_PLATFORM "DESKTOP" CACHE STRING "Select build target platform")
set_property(CACHE BUILD_TARGET_PLATFORM PROPERTY STRINGS "ANDROID" "IOS" "DESKTOP")

if(BUILD_TARGET_PLATFORM STREQUAL "ANDROID")
    include(${CMAKE_CURRENT_LIST_DIR}/android.cmake)
    if(ANDROID_EP_PREFIX)
      set(EP_PREFIX "${ANDROID_EP_PREFIX}/${ANDROID_ABI}" CACHE INTERNAL "External project prefix")
    endif()
elseif(BUILD_TARGET_PLATFORM STREQUAL "IOS")
    include(${CMAKE_CURRENT_LIST_DIR}/ios.cmake)
else() # DESKTOP
    if(OSX_FRAMEWORK AND (BUILD_SHARED_LIBS OR BUILD_STATIC_LIBS))
      message(FATAL_ERROR "Only OSX_FRAMEWORK key or any or both BUILD_SHARED_LIBS
                          and BUILD_STATIC_LIBS keys are permitted")
    endif()
    set(DESKTOP ON CACHE INTERNAL "Desktop build")
endif()

if(OSX_FRAMEWORK)
    set(INSTALL_BIN_DIR "bin" CACHE INTERNAL "Installation directory for executables" FORCE)
    set(INSTALL_LIB_DIR "Library/Frameworks" CACHE INTERNAL "Installation directory for libraries" FORCE)
    set(INSTALL_INC_DIR "${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Headers" CACHE INTERNAL "Installation directory for headers" FORCE)
    set(INSTALL_CMAKECONF_DIR ${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Resources/CMake CACHE INTERNAL "Installation directory for cmake config files" FORCE)
    set(SKIP_INSTALL_HEADERS ON CACHE INTERNAL "OSX SKIP INSTALL HEADERS")
    set(SKIP_INSTALL_EXECUTABLES ON CACHE INTERNAL "OSX SKIP INSTALL EXECUTABLES")
    set(SKIP_INSTALL_FILES ON CACHE INTERNAL "OSX SKIP INSTALL Files")
    set(SKIP_INSTALL_EXPORT ON CACHE INTERNAL "OSX SKIP INSTALL export")
    set(CMAKE_MACOSX_RPATH ON CACHE INTERNAL "OSX CMAKE MACOSX RPATH")
else()
    include(GNUInstallDirs)
    set(INSTALL_BIN_DIR ${CMAKE_INSTALL_BINDIR} CACHE INTERNAL "Installation directory for executables" FORCE)
    set(INSTALL_LIB_DIR ${CMAKE_INSTALL_LIBDIR} CACHE INTERNAL "Installation directory for libraries" FORCE)
    set(INSTALL_INC_DIR ${CMAKE_INSTALL_INCLUDEDIR} CACHE INTERNAL "Installation directory for headers" FORCE)
    set(INSTALL_DATA_DIR ${CMAKE_INSTALL_DATADIR} CACHE INTERNAL "Installation directory for shared files" FORCE)
    set(INSTALL_CMAKECONF_DIR ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME}/CMake CACHE INTERNAL "Installation directory for cmake config files" FORCE)
endif()

if(CMAKE_BUILD_TYPE STREQUAL Debug)
    add_definitions(-D_DEBUG)
endif()

configure_file(${CMAKE_CURRENT_LIST_DIR}/uninstall.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/uninstall.cmake IMMEDIATE @ONLY)

if(IOS)
    configure_file("${CMAKE_CURRENT_LIST_DIR}/Info.plist.in"
                 "${CMAKE_BINARY_DIR}/ios/Info.plist")
elseif(APPLE)
    configure_file("${CMAKE_CURRENT_LIST_DIR}/Info.plist.in"
                 "${CMAKE_BINARY_DIR}/osx/Info.plist")
endif()

set(CMAKE_POSITION_INDEPENDENT_CODE ON CACHE INTERNAL "POSITION INDEPENDENT CODE")

if(WIN32)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib CACHE INTERNAL "LIBRARY OUTPUT DIRECTORY")
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib CACHE INTERNAL "ARCHIVE OUTPUT DIRECTORY")
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin CACHE INTERNAL "RUNTIME OUTPUT DIRECTORY")
endif()
