include(${CMAKE_CURRENT_LIST_DIR}/install.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/pack.cmake)


function(create_borsch_package PACKAGE_NAME PACKAGE_VENDOR VERSION TARGETS HEADERS)
    string(TOUPPER ${PACKAGE_NAME} PACKAGE_UPPER_NAME)

    include(${CMAKE_CURRENT_FUNCTION_LIST_DIR}/base.cmake)

    add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/uninstall.cmake)

    create_borsch_install_rules(${PACKAGE_UPPER_NAME} ${TARGETS} ${HEADERS})
    pack(${PACKAGE_UPPER_NAME} ${PACKAGE_VENDOR} ${VERSION})
endfunction(create_borsch_package)
