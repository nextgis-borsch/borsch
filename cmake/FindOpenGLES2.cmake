#-------------------------------------------------------------------
# This file is stolen from part of the CMake build system for OGRE (Object-oriented Graphics Rendering Engine) http://www.ogre3d.org/
#
# Modified by Dmitry Baryshnikov (NextGIS), bishop.dev@gmail.com
#
# Copyright (C) 2016 NextGIS, info@nextgis.comm
#
# The contents of this file are placed in the public domain. Feel
# free to make use of it in any way you like.
#-------------------------------------------------------------------

# - Try to find OpenGLES and EGL
# Once done this will define
#
#  OPENGLES2_FOUND        - system has OpenGLES
#  OPENGLES2_INCLUDE_DIRS - the GL include directory
#  OPENGLES2_LIBRARIES    - Link these to use OpenGLES

if(IOS)
    find_path(OPENGLES2_INCLUDE_DIR NAMES OpenGLES/ES2/gl.h)
    set(OPENGLES2_LIBRARY "-framework OpenGLES")
else()
    find_path(OPENGLES2_INCLUDE_DIR NAMES GLES2/gl2.h)
    find_library(OPENGLES2_LIBRARY NAMES GLESv2)
endif()

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(OpenGLES2 DEFAULT_MSG OPENGLES2_INCLUDE_DIR OPENGLES2_LIBRARY)

set(OPENGLES2_INCLUDE_DIRS ${OPENGLES2_INCLUDE_DIR})
set(OPENGLES2_LIBRARIES ${OPENGLES2_LIBRARY})

mark_as_advanced(OPENGLES2_INCLUDE_DIR OPENGLES2_LIBRARY)

#
# if(WIN32)
# 	if(CYGWIN)
# 		find_path(OPENGLES2_INCLUDE_DIRS GLES2/gl2.h)
# 		find_library(OPENGLES2_LIBRARY libGLESv2)
# 	endif()
# elseif(APPLE)
# 	create_search_paths(/Developer/Platforms)
# 	findpkg_framework(OpenGLES2)
# 	set(OPENGLES2_LIBRARY "-framework OpenGLES")
# else()
# 	find_path(OPENGLES2_INCLUDE_DIRS GLES2/gl2.h
# 		PATHS /usr/openwin/share/include
# 			/opt/graphics/OpenGL/include
# 			/opt/vc/include
# 			/usr/X11R6/include
# 			/usr/include
# 	)
#
#
# 	find_library(OPENGLES2_LIBRARY
#         NAMES GLESv2 glesv2
# 		PATHS /opt/graphics/OpenGL/lib
# 			/usr/openwin/lib
# 			/usr/shlib /usr/X11R6/lib
# 			/opt/vc/lib
# 			/usr/lib/aarch64-linux-gnu
# 			/usr/lib/arm-linux-gnueabihf
#             /usr/lib/x86_64-linux-gnu
#             /usr/lib
#         )
# endif()
#
# set(OPENGLES2_LIBRARIES ${OPENGLES2_LIBRARIES} ${OPENGLES2_LIBRARY})
#
# include(FindPackageHandleStandardArgs)
# FIND_PACKAGE_HANDLE_STANDARD_ARGS(OPENGLES2 DEFAULT_MSG OPENGLES2_INCLUDE_DIRS OPENGLES2_LIBRARIES)
#
# mark_as_advanced(OPENGLES2_INCLUDE_DIRS OPENGLES2_LIBRARIES)
