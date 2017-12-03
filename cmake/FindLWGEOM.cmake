# Locate LWGEOM
# This module defines
# LWGEOM_LIBRARY
# LWGEOM_FOUND, if false, do not try to link to expat
# LWGEOM_INCLUDE_DIR, where to find the headers
#
# $LWGEOM_DIR is an environment variable that would
# correspond to the ./configure --prefix=$LWGEOM_DIR

FIND_PATH(LWGEOM_INCLUDE_DIR liblwgeom.h
    $ENV{LWGEOM_DIR}/include
    $ENV{LWGEOM_DIR}/Source/lib #Windows Binary Installer
    $ENV{LWGEOM_DIR}
    ~/Library/Frameworks
    /Library/Frameworks
    /usr/local/include
    /usr/include
    /sw/include # Fink
    /opt/local/include # DarwinPorts
    /opt/csw/include # Blastwave
    /opt/include
    /usr/freeware/include
    /devel
)

FIND_LIBRARY(LWGEOM_LIBRARY
    NAMES lwgeom
    PATHS
    $ENV{LWGEOM_DIR}/lib
    $ENV{LWGEOM_DIR}/bin #Windows Binary Installer
    $ENV{LWGEOM_DIR}
    ~/Library/Frameworks
    /Library/Frameworks
    /usr/local/lib
    /usr/lib
    /sw/lib
    /opt/local/lib
    /opt/csw/lib
    /opt/lib
    /usr/freeware/lib64
)

SET(LWGEOM_FOUND "NO")
IF(LWGEOM_LIBRARY AND LWGEOM_INCLUDE_DIR)
    SET(LWGEOM_FOUND "YES")
ENDIF(LWGEOM_LIBRARY AND LWGEOM_INCLUDE_DIR)


