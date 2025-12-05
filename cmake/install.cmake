function(create_borsch_install_rules PACKAGE_UPPER_NAME TARGETS HEADERS)
    if(OSX_FRAMEWORK)
        set(INSTALL_LIB_DIR "Library/Frameworks" CACHE INTERNAL "Installation directory for libraries" FORCE)
        set(INSTALL_CMAKECONF_DIR ${INSTALL_LIB_DIR}/${PACKAGE_UPPER_NAME}.framework/Resources/CMake CACHE INTERNAL "Installation directory for cmake config files" FORCE)
        set(INSTALL_INC_DIR ${INSTALL_LIB_DIR}/${PACKAGE_UPPER_NAME}.framework/Headers CACHE INTERNAL "Installation directory for headers" FORCE)
        set(SKIP_INSTALL_EXPORT ON)
        set(SKIP_INSTALL_HEADERS ON)
        set(SKIP_INSTALL_FILES ON)
        set(CMAKE_MACOSX_RPATH ON)
    else()
        include(GNUInstallDirs)

        set(INSTALL_BIN_DIR ${CMAKE_INSTALL_BINDIR} CACHE INTERNAL "Installation directory for executables" FORCE)
        set(INSTALL_LIB_DIR ${CMAKE_INSTALL_LIBDIR} CACHE INTERNAL "Installation directory for libraries" FORCE)
        set(INSTALL_INC_DIR ${CMAKE_INSTALL_INCLUDEDIR} CACHE INTERNAL "Installation directory for headers" FORCE)
        set(INSTALL_MAN_DIR ${CMAKE_INSTALL_MANDIR} CACHE INTERNAL "Installation directory for manual pages" FORCE)
        set(INSTALL_PKGCONFIG_DIR "${INSTALL_LIB_DIR}/pkgconfig" CACHE INTERNAL "Installation directory for pkgconfig (.pc) files" FORCE)
        set(INSTALL_CMAKECONF_DIR ${CMAKE_INSTALL_DATADIR}/${PACKAGE_UPPER_NAME}/CMake CACHE INTERNAL "Installation directory for cmake config files" FORCE)
    endif()
    
    configure_file(${CMAKE_CURRENT_FUNCTION_LIST_DIR}/PackageConfig.cmake.in
        ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake @ONLY)

    if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL)
        install(TARGETS ${TARGETS}
            EXPORT ${PACKAGE_UPPER_NAME}Targets
            RUNTIME DESTINATION ${INSTALL_BIN_DIR} # at least for dlls
            ARCHIVE DESTINATION ${INSTALL_LIB_DIR}
            LIBRARY DESTINATION ${INSTALL_LIB_DIR}
            INCLUDES DESTINATION ${INSTALL_INC_DIR}
            FRAMEWORK DESTINATION ${INSTALL_LIB_DIR}
        )

        # Install the <Package>Config.cmake
        install(FILES
            ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake
            DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev
        )

        # Install the export set for use with the install-tree
        install(EXPORT ${PACKAGE_UPPER_NAME}Targets DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev)
    endif()

    if(NOT SKIP_INSTALL_HEADERS AND NOT SKIP_INSTALL_ALL)
        install(FILES ${HEADERS} DESTINATION ${INSTALL_INC_DIR} COMPONENT dev)
    endif()

endfunction(create_borsch_install_rules)
