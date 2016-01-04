# Common cmake scripts
This is common cmake scripts for building system. 
Now two main files created **find_anyproject.cmake** and **find_extproject.cmake**.

find_anyproject.cmake - have to functions: find_anyproject and target_link_extlibraries. 

The first one try to find_package locally. If no package found user can select to use external project. The find_extproject.cmake used for it.

The second one used to link target libraries from both local or external packages. 

There are set of FindExtxxx.cmake files for external repositories details and some additional logic.

# Use cases

To use this scripts one have to put the cmake folder to the sources.
Than the folder need to be added to modules path:
```
# set path to additional CMake modules
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
```

Than a few lines of code need to add some external project:

```
include(find_anyproject)

# TIFF support - required, default=ON
find_anyproject(TIFF REQUIRED)
```

Some additional parameters supported. From find_project support:
* EXACT
* QUIET
* MODULE
* REQUIRED
* COMPONENTS

Also the version can be specified via VERSION <version>

Any other parameters will be forward to the external project. The important parameter is **CMAKE_ARGS**.

```
find_anyproject(CURL REQUIRED CMAKE_ARGS
      -DBUILD_CURL_EXE=OFF
      -DCURL_DISABLE_FTP=ON
      -DCURL_DISABLE_LDAP=ON
      -DCURL_DISABLE_TELNET=ON
      -DCURL_DISABLE_DICT=ON
      -DCURL_DISABLE_FILE=ON
      -DCURL_DISABLE_TFTP=ON
      -DCURL_DISABLE_LDAPS=ON
      -DCURL_DISABLE_RTSP=ON
      -DCURL_DISABLE_PROXY=ON
      -DCURL_DISABLE_POP3=ON
      -DCURL_DISABLE_IMAP=ON
      -DCURL_DISABLE_SMTP=ON
      -DCURL_DISABLE_GOPHER=ON
      -DCURL_DISABLE_CRYPTO_AUTH=OFF
      -DENABLE_IPV6=OFF
      -DENABLE_MANUAL=OFF
      -DCMAKE_USE_OPENSSL=OFF
      -DCMAKE_USE_LIBSSH2=OFF)
```      

The final step is to link target libraries:

```
target_link_extlibraries(${LIB_NAME}) 
```

# Cmaked libraries

This is a table of available libraries.

| Repository | Cmaked  | OS tested | Notes |
|---|:-:|---|---|
| [lib_z](https://github.com/nextgis-extra/lib_z)  | yes | Linux, Windows  |   |
| [lib_lzma](https://github.com/nextgis-extra/lib_lzma) | yes   | Linux, Windows |  |
| [lib_xml2](https://github.com/nextgis-extra/lib_xml2) | yes   | Linux, Windows |  |
| [lib_curl](https://github.com/nextgis-extra/lib_curl) | no   | |  |
| [lib_geotiff](https://github.com/nextgis-extra/lib_geotiff) | yes   | Linux |  |
| [lib_tiff](https://github.com/nextgis-extra/lib_tiff) | yes   | Linux |  |
| [lib_jpeg](https://github.com/nextgis-extra/lib_jpeg) | yes   | Linux, Windows |  |
| [lib_jbig](https://github.com/nextgis-extra/lib_jbig) | yes   | Linux, Windows |  |
| [lib_iconv](https://github.com/nextgis-extra/lib_iconv) | yes   | Linux, Windows |  |
| [lib_gdal](https://github.com/nextgis-extra/lib_gdal) | no   | |  |
| [lib_openssl](https://github.com/nextgis-extra/lib_openssl) | yes   | |  |
| [lib_jsonc](https://github.com/nextgis-extra/lib_jsonc) | no   | |  |
| [lib_expat](https://github.com/nextgis-extra/lib_expat) | no   | |  |
| [lib_proj](https://github.com/nextgis-extra/lib_proj) | yes   | Linux |  |
| [lib_png](https://github.com/nextgis-extra/lib_png) | no   | |  |
| [lib_hdf4](https://github.com/nextgis-extra/lib_hdf4) | yes | Linux |  |
| [lib_szip](https://github.com/nextgis-extra/lib_szip) | no   | |  |

# License

All scripts are licensed under GNU GPL v.2. 

# Notes

* There is additional util.cmake file for pretty print of version information to the console. 

* MSVC 2013 update 2 and later have enough C99 support to build under Windows.
