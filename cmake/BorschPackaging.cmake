include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
include(${CMAKE_CURRENT_LIST_DIR}/version.cmake)


function(generate_version_file MAJOR MINOR PATCH PACKAGE_TIMESTAMP_FILE)
    write_version(${PACKAGE_TIMESTAMP_FILE} ${MAJOR} ${MINOR} ${PATCH})
endfunction(generate_version_file MAJOR MINOR PATCH)


function(_to_package_upper_name NAME OUT_VAR)
    string(TOUPPER "${NAME}" temp)
    string(REPLACE "-" "_" temp "${temp}")
    set(${OUT_VAR} "${temp}" PARENT_SCOPE)
endfunction()

function(_create_target_aliases PACKAGE_NAME TARGET OUT_VAR)
    set(name_orig "${PACKAGE_NAME}")
    string(TOLOWER "${name_orig}" name_lower)
    string(TOUPPER "${name_orig}" name_upper)

    set(target_orig "${TARGET}")
    string(TOLOWER "${target_orig}" target_lower)

    get_target_property(_aliased ${TARGET} ALIASED_TARGET)
    if(_aliased)
        set(TARGET ${_aliased})
    endif()

    set(alias_candidates
        "${target_lower}"                         # mylib
        "${name_orig}::${target_orig}"            # MyLib1::MyLib
        "${name_orig}::${target_lower}"           # MyLib1::mylib
        "${name_lower}::${target_orig}"           # mylib1::MyLib
        "${name_lower}::${target_lower}"          # mylib1::mylib
        "${name_upper}::${target_orig}"           # MYLIB1::MyLib
        "${name_upper}::${target_lower}"          # MYLIB1::mylib
    )

    set(added_targets "")

    foreach(alias IN LISTS alias_candidates)
        if(TARGET "${alias}")
            get_target_property(tgt_type "${alias}" TYPE)
            if(tgt_type STREQUAL "SHARED_LIBRARY")
                list(APPEND added_targets "${alias}")
            endif()
        else()
            add_library("${alias}" ALIAS "${TARGET}")
            list(APPEND added_targets "${alias}")
        endif()
    endforeach()

    set(${OUT_VAR} "${added_targets}" PARENT_SCOPE)
endfunction()

function(_separate_targets_and_aliases _input_list _out_real _out_aliases)
    set(_real_targets "")
    set(_aliases "")

    foreach(_item IN LISTS _input_list)
        if(TARGET ${_item})
            get_target_property(_aliased_name ${_item} ALIASED_TARGET)
            if(_aliased_name)
                list(APPEND _aliases ${_item})
            else() # _aliased_name STREQUAL "${_current}-NOTFOUND"
                list(APPEND _real_targets ${_item})
            endif()
        endif()
    endforeach()

    set(_additional_real "")
    foreach(_alias IN LISTS _aliases)
        set(_current ${_alias})
        get_target_property(_next_tgt ${_current} ALIASED_TARGET)
        if(_next_tgt STREQUAL "${_current}-NOTFOUND")
            break()
        else()
            set(_current ${_next_tgt})
        endif()
        set(_resolved ${_current})

        if(NOT _resolved IN_LIST _real_targets AND NOT _resolved IN_LIST _additional_real)
            list(APPEND _additional_real ${_resolved})
        endif()
    endforeach()

    set(_final_real ${_real_targets} ${_additional_real})

    set(${_out_real} ${_final_real} PARENT_SCOPE)
    set(${_out_aliases} ${_aliases} PARENT_SCOPE)
endfunction()


function(_move_targets_to_bin TARGETS)
    if(NOT TARGETS)
        return()
    endif()

    set(script_file "${PROJECT_BINARY_DIR}/move_targets_to_bin.cmake")
    set(script_content "")

    foreach(tgt ${TARGETS})
        get_target_property(out_name ${tgt} OUTPUT_NAME)
        if(NOT out_name)
            set(out_name "${tgt}")
        endif()

        string(APPEND script_content
            "# Move ${tgt} from ${CMAKE_INSTALL_LIBDIR} to ${CMAKE_INSTALL_BINDIR}\n"
            "if(EXISTS \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}\")\n"
            "    file(GLOB found_files \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/${out_name}*\")\n"
            "    if(found_files)\n"
            "        file(COPY \${found_files} DESTINATION \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}\")\n"
            "        file(REMOVE \${found_files})\n"
            "        message(STATUS \"Moved ${tgt} from lib to bin\")\n"
            "    endif()\n"
            "endif()\n\n"
        )
    endforeach()

    file(WRITE "${script_file}" "${script_content}")
    install(SCRIPT "${script_file}")
endfunction()


function(create_borsch_package PACKAGE_NAME)
    set(options)
    set(oneValueArgs VERSION COMPATIBILITY TIMESTAMP_FILE VENDOR HEADERS_PREFIX HEADERS_DIRS_PREFIX)
    set(multiValueArgs LIBRARIES EXECUTABLES HEADERS HEADERS_DIRS)
    cmake_parse_arguments(PARSE_ARGV 1 PACKAGE "${options}" "${oneValueArgs}" "${multiValueArgs}")

    _to_package_upper_name("${PACKAGE_NAME}" PACKAGE_UPPER_NAME)

    # ----- TIMESTAMP -----
    if(NOT PACKAGE_TIMESTAMP_FILE)
        set(PACKAGE_TIMESTAMP_FILE ${CMAKE_CURRENT_LIST_FILE})
    endif()

    # ----- VERSION -----
    if(PACKAGE_VERSION)
        string(REPLACE "." ";" VERSION_LIST "${PACKAGE_VERSION}")
        list(LENGTH VERSION_LIST _ver_len)
        if(_ver_len GREATER 2)
            list(GET VERSION_LIST 0 MAJOR)
            list(GET VERSION_LIST 1 MINOR)
            list(GET VERSION_LIST 2 PATCH)
        elseif(_ver_len EQUAL 2)
            list(GET VERSION_LIST 0 MAJOR)
            list(GET VERSION_LIST 1 MINOR)
            set(PATCH 0)
        elseif(_ver_len EQUAL 1)
            list(GET VERSION_LIST 0 MAJOR)
            set(MINOR 0)
            set(PATCH 0)
        else()
            message(FATAL_ERROR "Invalid VERSION string: ${PACKAGE_VERSION}")
        endif()

        generate_version_file(${MAJOR} ${MINOR} ${PATCH} ${PACKAGE_TIMESTAMP_FILE})
    elseif(PROJECT_VERSION)
        generate_version_file(${PROJECT_VERSION_MAJOR} ${PROJECT_VERSION_MINOR} ${PROJECT_VERSION_PATCH} ${PACKAGE_TIMESTAMP_FILE})
    else()
        message(FATAL_ERROR "VERSION argument is required")
    endif()

    # ----- COMPATIBILITY -----
    if(PACKAGE_COMPATIBILITY)
        set(PACKAGE_COMPATIBILITY_VAR "${PACKAGE_COMPATIBILITY}")
    else()
        set(PACKAGE_COMPATIBILITY_VAR "AnyNewerVersion")
    endif()

    write_basic_package_version_file(
        "${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}ConfigVersion.cmake"
        VERSION ${PACKAGE_VERSION}
        COMPATIBILITY ${PACKAGE_COMPATIBILITY_VAR}
    )

    # ----- VENDOR -----
    if(PACKAGE_VENDOR)
        set(PACKAGE_VENDOR_CPACK "${PACKAGE_VENDOR}")
    elseif(DEFINED PACKAGE_VENDOR AND NOT PACKAGE_VENDOR STREQUAL "")
        set(PACKAGE_VENDOR_CPACK "${PACKAGE_VENDOR}")
    else()
        set(PACKAGE_VENDOR_CPACK "NextGIS")
    endif()

    # ----- LIBRARIES / EXECUTABLES -----
    _separate_targets_and_aliases(${PACKAGE_LIBRARIES} PACKAGE_TARGETS_LIBRARIES PACKAGE_TARGETS_ALIASES)

    list(REMOVE_DUPLICATES PACKAGE_TARGETS_LIBRARIES)

    set(PACKAGE_TARGETS_RAW ${PACKAGE_TARGETS_LIBRARIES})
    list(APPEND PACKAGE_TARGETS_RAW ${PACKAGE_TARGETS_ALIASES})

    set(PACKAGE_ALIASES "")
    foreach(_target ${PACKAGE_TARGETS_RAW})
        _create_target_aliases(${PACKAGE_NAME} ${_target} _aliases)
        list(APPEND PACKAGE_ALIASES ${_aliases})
    endforeach()

    list(APPEND PACKAGE_ALIASES ${PACKAGE_TARGETS_ALIASES})
    list(REMOVE_DUPLICATES PACKAGE_ALIASES)
    
    set(PACKAGE_ALIASES_INIT "")
    foreach(alias ${PACKAGE_ALIASES})
        get_target_property(_aliased_target ${alias} ALIASED_TARGET)
        if(_aliased_target)
            set(PACKAGE_ALIASES_INIT 
                "${PACKAGE_ALIASES_INIT}\nadd_library(${alias} ALIAS ${_aliased_target})"
            )
        endif()
    endforeach()

    set(PACKAGE_REAL_TARGETS ${PACKAGE_TARGETS_LIBRARIES} ${PACKAGE_EXECUTABLES})

    if(PACKAGE_REAL_TARGETS)
        _move_targets_to_bin("${PACKAGE_REAL_TARGETS}")
    endif()

    # ----- HEADERS -----
    if(NOT DEFINED SKIP_INSTALL_HEADERS OR NOT SKIP_INSTALL_HEADERS)
        if(PACKAGE_HEADERS)
            if(PACKAGE_HEADERS_PREFIX)
                set(_headers_dest "${CMAKE_INSTALL_INCLUDEDIR}/${PACKAGE_HEADERS_PREFIX}")
            else()
                set(_headers_dest "${CMAKE_INSTALL_INCLUDEDIR}")
            endif()
            install(FILES ${PACKAGE_HEADERS}
                DESTINATION "${_headers_dest}"
                COMPONENT dev
            )
        endif()

        if(PACKAGE_HEADERS_DIRS)
            if(PACKAGE_HEADERS_DIRS_PREFIX)
                set(_hdirs_dest "${CMAKE_INSTALL_INCLUDEDIR}/${PACKAGE_HEADERS_DIRS_PREFIX}")
            else()
                set(_hdirs_dest "${CMAKE_INSTALL_INCLUDEDIR}")
            endif()
            foreach(dir ${PACKAGE_HEADERS_DIRS})
                install(DIRECTORY "${dir}"
                    DESTINATION "${_hdirs_dest}"
                    COMPONENT dev
                    FILES_MATCHING PATTERN "*.h"
                )
                install(DIRECTORY "${dir}"
                    DESTINATION "${_hdirs_dest}"
                    COMPONENT dev
                    FILES_MATCHING PATTERN "*.hpp"
                )
                install(DIRECTORY "${dir}"
                    DESTINATION "${_hdirs_dest}"
                    COMPONENT dev
                    FILES_MATCHING PATTERN "*.hxx"
                )
            endforeach()
        endif()
    else()
        install(CODE "
            if(EXISTS \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_INCLUDEDIR}\")
                file(REMOVE_RECURSE \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_INCLUDEDIR}\")
                message(STATUS \"Removed include directory because SKIP_INSTALL_HEADERS is ON\")
            endif()
        ")
    endif()

    # ----- CMake-configs and targets -----
    set(INSTALL_CMAKECONF_DIR ${CMAKE_INSTALL_DATADIR}/${PACKAGE_UPPER_NAME}/CMake
        CACHE INTERNAL "Installation directory for cmake config files" FORCE)
    set(INSTALL_BIN_DIR ${CMAKE_INSTALL_BINDIR} CACHE PATH "Binary install dir" FORCE)
    set(INSTALL_LIB_DIR ${CMAKE_INSTALL_LIBDIR} CACHE PATH "Library install dir" FORCE)
    set(INSTALL_INC_DIR ${CMAKE_INSTALL_INCLUDEDIR} CACHE PATH "Include install dir" FORCE)

    configure_file(${CMAKE_CURRENT_FUNCTION_LIST_DIR}/BorschPackageConfig.cmake.in
        ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake @ONLY)

    if(PACKAGE_REAL_TARGETS)
        export(TARGETS ${PACKAGE_REAL_TARGETS}
            FILE ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Targets.cmake
        )

        install(TARGETS ${PACKAGE_REAL_TARGETS}
            EXPORT ${PACKAGE_UPPER_NAME}Targets
            RUNTIME DESTINATION ${INSTALL_BIN_DIR}
            ARCHIVE DESTINATION ${INSTALL_LIB_DIR}
            LIBRARY DESTINATION ${INSTALL_LIB_DIR}
            INCLUDES DESTINATION ${INSTALL_INC_DIR}
            FRAMEWORK DESTINATION ${INSTALL_LIB_DIR}
        )
        install(EXPORT ${PACKAGE_UPPER_NAME}Targets
            DESTINATION ${INSTALL_CMAKECONF_DIR}
            COMPONENT dev
        )
    endif()

    install(FILES
        ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake
        ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}ConfigVersion.cmake
        DESTINATION ${INSTALL_CMAKECONF_DIR}
        COMPONENT dev
    )

    # ----- CPack -----
    set(CPACK_PACKAGE_NAME "${PACKAGE_NAME}" CACHE STRING "CPack package name" FORCE)
    set(CPACK_PACKAGE_VENDOR "${PACKAGE_VENDOR_CPACK}" CACHE STRING "CPack package vendor" FORCE)
    set(CPACK_PACKAGE_VERSION "${PACKAGE_VERSION}" CACHE STRING "CPack package version" FORCE)
    set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PACKAGE_NAME} Installation" CACHE STRING "Description" FORCE)
    set(CPACK_PACKAGE_RELOCATABLE TRUE CACHE BOOL "" FORCE)
    set(CPACK_ARCHIVE_COMPONENT_INSTALL ON CACHE BOOL "" FORCE)
    set(CPACK_GENERATOR "ZIP" CACHE STRING "" FORCE)
    set(CPACK_MONOLITHIC_INSTALL ON CACHE BOOL "" FORCE)
    set(CPACK_STRIP_FILES TRUE CACHE BOOL "" FORCE)

    get_cpack_filename(${PACKAGE_VERSION} PROJECT_CPACK_FILENAME)
    set(CPACK_PACKAGE_FILE_NAME ${PROJECT_CPACK_FILENAME} CACHE STRING "" FORCE)

    include(CPack)
endfunction()
