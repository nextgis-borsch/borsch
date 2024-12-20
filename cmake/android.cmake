################################################################################
#  Project: libngstore
#  Purpose: NextGIS store and visualisation support library
#  Author: Dmitry Baryshnikov, dmitry.baryshnikov@nextgis.com
#  Language: C/C++
################################################################################
#  GNU Lesser General Public Licens v3
#
#  Copyright (c) 2016 NextGIS, <info@nextgis.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

if(NOT CMAKE_BUILD_TYPE STREQUAL "Debug" AND NOT CMAKE_BUILD_TYPE STREQUAL "Release")
    message(FATAL_ERROR "Android not support build type ${CMAKE_BUILD_TYPE}")
endif()

# if(NOT BUILD_STATIC_LIBS)
#     message(FATAL_ERROR "Android not support shared or framework builds")
# endif()

if(NOT CMAKE_TOOLCHAIN_FILE)
    set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/cmake/android.toolchain.cmake
        CACHE PATH "Select android toolchain file path")
endif()

if(NOT ANDROID_ABI)
    set(ANDROID_ABI "armeabi-v7a" CACHE STRING "Select Android ABI")
    set_property(CACHE ANDROID_ABI PROPERTY STRINGS "armeabi" "armeabi-v7a"
        "armeabi-v7a with NEON" "armeabi-v7a with VFPV3" "armeabi-v6 with VFP"
        "x86" "mips" "arm64-v8a" "x86_64" "mips64")
endif()

#set(ANDROID_APK_API_LEVEL "10" CACHE STRING "Android APK API level")
#set(ANDROID_APK_INSTALL "0" CACHE BOOL "Install created apk file on the device automatically?")
#set(ANDROID_APK_RUN "0" CACHE BOOL "Run created apk file on the device automatically? (installs it automatically as well, \"ANDROID_APK_INSTALL\"-option is ignored)")
#set(ANDROID_APK_SIGNER_KEYSTORE	"~/my-release-key.keystore" CACHE STRING "Keystore for signing the apk file (only required for release apk)")
#set(ANDROID_APK_SIGNER_ALIAS "myalias" CACHE STRING "Alias for signing the apk file (only required for release apk)")
