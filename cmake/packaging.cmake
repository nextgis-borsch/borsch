include(${CMAKE_CURRENT_LIST_DIR}/install.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/pack.cmake)
include(CMakePackageConfigHelpers)

# Adds install and packaging rules for package with name PACKAGE_NAME using the given VENDOR, VERSION, TARGETS and HEADERS
# Usage example:
# ```
# create_borsch_package(MyPackage
#     VENDOR MyPackageVendor
#     VERSION 1.2.3
#     TARGETS target1 target2
#     HEADERS header1.h header2.h header3.h
# )
# ```
#
# Or, preferably, using lists:
# ```
# set(TARGETS target1 target2)
# set(HEADERS header1.h header2.h header3.h)
# create_borsch_package(MyPackage
#     VENDOR MyPackageVendor
#     VERSION 1.2.3
#     TARGETS ${TARGETS}
#     HEADERS ${HEADERS}
# )
# ```
function(create_borsch_package PACKAGE_NAME VENDOR VERSION TARGETS COMPATIBILITY HEADERS HEADERS_DIRS)
    cmake_parse_arguments(
        PARSE_ARGV 1
        PACKAGE
        ""
        "VENDOR;VERSION;COMPATIBILITY"
        "TARGETS;HEADERS;HEADERS_DIRS"
    )

    string(TOUPPER ${PACKAGE_NAME} PACKAGE_UPPER_NAME)
    string(TOLOWER ${PACKAGE_NAME} PACKAGE_LOWER_NAME)

    include(${CMAKE_CURRENT_FUNCTION_LIST_DIR}/base.cmake)

    add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/uninstall.cmake)

    if(NOT DEFINED PACKAGE_VENDOR)
        set(PACKAGE_VENDOR NextGIS)
    endif()
    
    if(NOT DEFINED PACKAGE_BUGREPORT)
        set(PACKAGE_BUGREPORT info@nextgis.com)
    endif()

    if(NOT DEFINED PACKAGE_COMPATIBILITY)
        set(PACKAGE_COMPATIBILITY AnyNewerVersion)
    endif()

    write_basic_package_version_file(
        "${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}ConfigVersion.cmake"
        VERSION ${PACKAGE_VERSION}
        COMPATIBILITY ${PACKAGE_COMPATIBILITY}
    )

    create_borsch_install_rules(${PACKAGE_UPPER_NAME}
        TARGETS ${PACKAGE_TARGETS}
        HEADERS ${PACKAGE_HEADERS}
        HEADERS_DIRS ${PACKAGE_HEADERS_DIRS}
    )

    pack(${PACKAGE_UPPER_NAME} ${PACKAGE_VENDOR} ${PACKAGE_VERSION})
endfunction(create_borsch_package)
