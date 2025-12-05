include(${CMAKE_CURRENT_LIST_DIR}/install.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/pack.cmake)

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
function(create_borsch_package PACKAGE_NAME PACKAGE_VENDOR VERSION TARGETS HEADERS)
    cmake_parse_arguments(
        PARSE_ARGV 1
        ARG
        ""
        "VENDOR;VERSION"
        "TARGETS;HEADERS"
    )

    string(TOUPPER ${PACKAGE_NAME} PACKAGE_UPPER_NAME)

    include(${CMAKE_CURRENT_FUNCTION_LIST_DIR}/base.cmake)

    add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/uninstall.cmake)

    create_borsch_install_rules(${PACKAGE_UPPER_NAME} 
        TARGETS ${ARG_TARGETS}
        HEADERS ${ARG_HEADERS}
    )

    pack(${PACKAGE_UPPER_NAME} ${ARG_VENDOR} ${ARG_VERSION})
endfunction(create_borsch_package)
