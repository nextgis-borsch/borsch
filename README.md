# Introduction

Many C/C++ GIS libraries are usually built via autoconf/make/nmake/VC. While this is valid approach, we believe there is a better new alternative - CMake. NextGIS Borsch (http://nextgis.com/borsch) is a new build system that is

* a) easier to use,
* b) better solves dependencies and
* c) provides more uniform way of building packages.

Needed dependencies are automatically fetched from repositories. We’ve built an early prototype of such system and tested it on GDAL build process (over 50 core dependent libraries). Now a developer with only three lines of code in CMakeLists.txt for any project he is working on can add dependent GIS library. If needed library exists in the system the build system will use it, if not - it will be downloaded from Github. Our new build system works for both Windows, Linux and MacOS.

# Common CMake scripts

These are common cmake scripts for building system.
Now two main files created **FindAnyProject.cmake** and **FindExtProject.cmake**.

FindAnyProject.cmake - have two main functions: find_anyproject and target_link_extlibraries.

The first one tries to find_package locally. If no package found user can opt to use external project. The FindExtProject.cmake is used for this.

The second one is used to link target libraries from both local or external packages.

Finally, there are sets of FindExtxxx.cmake files for external repositories details and additional logic.

Two additional files are mandatory for Borsch v2 functionality: **JSONParser.cmake** and **util.cmake**:

JSONParser.cmake - functions needed for parse github REST API request results.

util.cmake - function need for form binary artifacts names and for use in  toolchains.

# Use cases

To use this scripts need to add cmake folder to the sources.
Then the folder needs to be added to modules path:

```cmake
# set path to additional CMake modules
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
```

Add external project with few lines of code:

```cmake
include(FindAnyProject)

# TIFF support - required, default=ON
find_anyproject(TIFF REQUIRED)
```

Some additional parameters are supported. From find_project support:
* EXACT
* QUIET
* MODULE
* REQUIRED
* COMPONENTS

Version can be specified via VERSION ``<version>``

Any other parameters will be forwarded to the external project. The important parameter is **CMAKE_ARGS**. Note: do not pass WITH_X options with CMAKE_ARGS, use set(WITH_X ...) instead.

```cmake
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

```cmake
target_link_extlibraries(${LIB_NAME})
```

# Cmaked libraries

This is a table of currently available libraries.

| # | Repository | Cmaked | OS tested | Notes |
|:-:|---|:-:|---|:---|
|1| [lib_z](https://github.com/nextgis-borsch/lib_z)  | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|2| [lib_lzma](https://github.com/nextgis-borsch/lib_lzma) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|3| [lib_xml2](https://github.com/nextgis-borsch/lib_xml2) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|4| [lib_curl](https://github.com/nextgis-borsch/lib_curl) | yes | Windows, Mac OS X |  [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|5| [lib_geotiff](https://github.com/nextgis-borsch/lib_geotiff) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|6| [lib_tiff](https://github.com/nextgis-borsch/lib_tiff) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|7| [lib_jpeg](https://github.com/nextgis-borsch/lib_jpeg) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|8| [lib_jbig](https://github.com/nextgis-borsch/lib_jbig) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|9| [lib_iconv](https://github.com/nextgis-borsch/lib_iconv) | yes | Windows | not needed on Mac OS, [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|10| [lib_gdal](https://github.com/nextgis-borsch/lib_gdal) | yes | Windows, Mac OS X | tests present |
|11| [lib_openssl](https://github.com/nextgis-borsch/lib_openssl) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|12| [lib_jsonc](https://github.com/nextgis-borsch/lib_jsonc) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|13| [lib_expat](https://github.com/nextgis-borsch/lib_expat) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|14| [lib_proj](https://github.com/nextgis-borsch/lib_proj) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|15| [lib_png](https://github.com/nextgis-borsch/lib_png) | yes | Windows, Mac OS X | tests present |
|16| [lib_hdf4](https://github.com/nextgis-borsch/lib_hdf4) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|17| lib_hdf5 | no |  | For GDAL Hierarchical Data Format Release 5 (HDF5) driver |
|18| [lib_szip](https://github.com/nextgis-borsch/lib_szip) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|19| [lib_hdfeos2](https://github.com/nextgis-borsch/lib_hdfeos2) | yes | Windows | tests present, 7 failed |
|20| [lib_geos](https://github.com/nextgis-borsch/lib_geos) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|21| lib_hdfeos5 | no | |  |
|22| lib_bpg | no | | For GDAL BPG (Better Portable Graphics) driver |
|23| lib_dap | no | | For GDAL DODS / OPeNDAP driver |
|24| lib_epsilon | no | | For GDAL Epsilon - Wavelet compressed images driver |
|25| lib_cfitsio | no | | For GDAL FITS (.fits) driver |
|26| [lib_sqlite3](https://github.com/nextgis-borsch/lib_sqlite) | yes | Windows, Mac OS X | For GDAL GeoPackage and other drivers, [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|27| [lib_gif](https://github.com/nextgis-borsch/lib_gif) | yes | Windows, Mac OS X | For GDAL GIF driver, [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|28| lib_netcdf | no | | For GDAL GMT Compatible netCDF driver |
|29| lib_grass | no | | For GDAL GRASS driver |
|30| lib_gta | no | | For GDAL Generic Tagged Arrays (.gta) driver |
|31| lib_jasper | no | | For GDAL JPEG2000 (.jp2, .j2k) driver |
|32| [lib_openjpeg](https://github.com/nextgis-borsch/lib_openjpeg) | yes | Windows, Mac OS X | For GDAL GeoPackage and other drivers, [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|33| lib_csf | no | | For GDAL PCRaster driver |
|34| lib_pdfium | no | | For GDAL Geospatial PDF driver |
|35| [lib_pq](https://github.com/nextgis-borsch/lib_pq) | yes | Windows, Mac OS X | For GDAL PostGIS Raster driver. [libpq CMakeLists.txt]( https://github.com/stalkerg/postgres_cmake/blob/cmake/src/interfaces/libpq/CMakeLists.txt) [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|36| lib_ras | no | | For GDAL Rasdaman driver |
|37| lib_webp | no | | For GDAL WEBP driver |
|38| lib_xerces | no | | For GDAL INTERLIS driver |
|39| [lib_kml](https://github.com/nextgis-borsch/lib_kml) | yes | Windows, Mac OS X | For GDAL LIBKML driver. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|40| lib_mongo | no | | For GDAL MongoDB driver |
|41| lib_mysql | no | | For GDAL MySQL driver |
|42| lib_pcidsk | no | | For GDAL PCI Geomatics Database File driver |
|43| lib_podofo | no | | For GDAL Geospatial PDF driver |
|44| [lib_freexl](https://github.com/nextgis-borsch/lib_freexl) | yes | Windows | For GDAL MS Excel format driver |
|45| [lib_spatialite](https://github.com/nextgis-borsch/lib_spatialite) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|46| [lib_spatialindex](https://github.com/nextgis-borsch/lib_spatialindex) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|47| [googletest](https://github.com/nextgis-borsch/googletest) | yes | Linux, Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|48| [lib_boost](https://github.com/nextgis-borsch/lib_boost) | yes | | Make only copies of headers from "boost/" without building libs |
|49| [lib_zip](https://github.com/nextgis-borsch/lib_zip) | yes | | |
|50| [lib_uv](https://github.com/nextgis-borsch/lib_uv) | yes | | |
|51| [lib_jpegturbo](https://github.com/nextgis-borsch/lib_jpegturbo) | no | | |
|52| [lib_variant](https://github.com/nextgis-borsch/lib_variant) | yes | | |
|53| [lib_rapidjson](https://github.com/nextgis-borsch/lib_rapidjson) | yes | | |
|54| [lib_nunicode](https://github.com/nextgis-borsch/lib_nunicode) | yes | | cmaked within the requirements of the mapbox |
|55| [lib_geojsonvt](https://github.com/nextgis-borsch/lib_geojsonvt) | yes | | |
|56| [postgis](https://github.com/nextgis-borsch/postgis) | yes | Linux | partially cmaked (except tiger and cgal) |
|57| [lib_opencad](https://github.com/nextgis-borsch/lib_opencad) | yes | Linux, Windows, Mac OS X | From GSoC2016, [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|58| [lib_uriparser](https://github.com/nextgis-borsch/lib_uriparser) | yes | Linux, Windows, Mac OS X | For lib_kml, [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|59| [numpy](https://github.com/nextgis-borsch/numpy) | yes | Windows, Mac OS X | Not a package but used for python dependency modules. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|60| [lib_ecw](https://github.com/nextgis-borsch/lib_ecw) | yes | Windows | Prebuild libraries for specific compiler and OS |
|61| [lib_mrsid](https://github.com/nextgis-borsch/lib_mrsid) | yes | Windows | Prebuild libraries for specific compiler and OS |
|62| [lib_gsl](https://github.com/nextgis-borsch/lib_gsl) | yes | Mac OS X | |
|63| [lib_qt4](https://github.com/nextgis-borsch/lib_qt4) | yes | Windows, Mac OS X | Sources received from Qt download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|64| [lib_qt5](https://github.com/nextgis-borsch/lib_qt5) | yes | Windows, Mac OS X | Sources received from Qt download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|65| [lib_qca](https://github.com/nextgis-borsch/lib_qca) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|66| [lib_qwt](https://github.com/nextgis-borsch/lib_qwt) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|67| [lib_qscintilla](https://github.com/nextgis-borsch/lib_qca) | yes | Windows, Mac OS X |  |
|68| [lib_cgal](https://github.com/nextgis-borsch/lib_cgal) | yes | | |
|69| [lib_agg](https://github.com/nextgis-borsch/lib_agg) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|70| [lib_freetype](https://github.com/nextgis-borsch/lib_freetype) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|71| [lib_qhull](https://github.com/nextgis-borsch/lib_qhull) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|72| [py_qt4](https://github.com/nextgis-borsch/py_qt4) | yes | Windows, Mac OS X | Sources received from Riverbank download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|73| [py_sip](https://github.com/nextgis-borsch/py_sip) | yes | Windows, Mac OS X | Sources received from Riverbank download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|74| [py_psycopg](https://github.com/nextgis-borsch/py_psycopg) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|75| [py_dateutil](https://github.com/nextgis-borsch/py_dateutil) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|76| [py_pygments](https://github.com/nextgis-borsch/py_pygments) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|77| [py_ows](https://github.com/nextgis-borsch/py_ows) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|78| [py_httplib](https://github.com/nextgis-borsch/py_httplib) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|79| [py_jinja](https://github.com/nextgis-borsch/py_jinja) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|80| [py_markupsafe](https://github.com/nextgis-borsch/py_markupsafe) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|81| [py_nose](https://github.com/nextgis-borsch/py_nose) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|82| [py_pytz](https://github.com/nextgis-borsch/py_pytz) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|83| [py_six](https://github.com/nextgis-borsch/py_six) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|84| [py_spatialite](https://github.com/nextgis-borsch/py_spatialite) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|85| [py_requests](https://github.com/nextgis-borsch/py_requests) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|86| [py_yaml](https://github.com/nextgis-borsch/py_yaml) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|87| [lib_yaml](https://github.com/nextgis-borsch/lib_yaml) | yes | Windows, Mac OS X | [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|88| [py_functools_lru_cache](https://github.com/nextgis-borsch/py_functools_lru_cache) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|89| [py_subprocess32](https://github.com/nextgis-borsch/py_subprocess32) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|90| [py_cycler](https://github.com/nextgis-borsch/py_cycler) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|91| [py_parsing](https://github.com/nextgis-borsch/py_parsing) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|92| [py_markupsafe](https://github.com/nextgis-borsch/py_markupsafe) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|93| [py_matplotlib](https://github.com/nextgis-borsch/py_matplotlib) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|94| [py_contextlib](https://github.com/nextgis-borsch/py_contextlib) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|95| [py_raven](https://github.com/nextgis-borsch/py_raven) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|96| [py_future](https://github.com/nextgis-borsch/py_future) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|97| [py_exifread](https://github.com/nextgis-borsch/py_exifread) | yes | Windows, Mac OS X | Sources received from pip download site and build using their own build system. [![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch) |
|98| [tests](https://github.com/nextgis-borsch/tests) | | | **Deprecated**. Tests should moved to their repositories |

# CMaked libraries requirements  

1. Make install instructions according to the GNU standard installation directories. Use ``include(GNUInstallDirs)``. For Mac OS X use option key OSX_FRAMEWORK=ON. Installation directories should be for frameworks: ``<CMAKE_INSTALL_PREFIX>/Library/Frameworks/<lib name in lower case without lib prefix>.framework`` and for applications:
``<CMAKE_INSTALL_PREFIX>/Applications/<app name>.app``
2. Add export instructions:

```cmake
# Add path to includes to build-tree export
target_include_directories(${TARGETS} PUBLIC
 $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
 $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)

# Add all targets to the build-tree export set
export(TARGETS ${TARGETS}
   FILE ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Targets.cmake)

if(REGISTER_PACKAGE)
   # Export the package for use from the build-tree
   # (this registers the build-tree with a global CMake-registry)
   export(PACKAGE ${PACKAGE_UPPER_NAME})
endif()

# Create the ZLIBConfig.cmake file
configure_file(cmake/PackageConfig.cmake.in
   ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake @ONLY)

if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL)
   # Install the <Package>Config.cmake
   install(FILES
     ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake
     DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev)

   # Install the export set for use with the install-tree
   install(EXPORT ${PACKAGE_UPPER_NAME}Targets DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev)
endif()
```

Also check install instruction has ``EXPORT`` and ``INCLUDES`` tags:

```cmake
install(TARGETS ${TARGETS}
    EXPORT ${PACKAGE_UPPER_NAME}Targets
    RUNTIME DESTINATION ${INSTALL_BIN_DIR}
    LIBRARY DESTINATION ${INSTALL_LIB_DIR}
    ARCHIVE DESTINATION ${INSTALL_LIB_DIR}
    INCLUDES DESTINATION ${INSTALL_INC_DIR}
    FRAMEWORK DESTINATION ${INSTALL_LIB_DIR} )
```    

This will export targets for build-tree use and for install-tree use.

3. All dependencies must be connected via find_anyproject (see "Borsch scripts").  
3.1. You need to add the relevant scripts from borsch to 'cmake' directory  
3.2. Add cmake instruction (if it is not present):

```cmake
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
```

4. Preferably cmake via include(util) should extract version from header file or another files and report it colored
5. Preferably add Findxxx.cmake with version check (see. [FindGEOS](https://github.com/nextgis-borsch/borsch/blob/master/cmake/FindGEOS.cmake) and [FindPROJ4](https://github.com/nextgis-borsch/borsch/blob/master/cmake/FindPROJ4.cmake))
6. Create FindExtxxx.cmake with library repository name and some optional variables

# Update library sources

Then new version of a library released, borsch need to be updated too.

1. Create tag for current version in repository and send it to server:

```bash
git tag -a v1.0.2.1 -m 'version 1.0.2a from 22 Jan 2015'
git push origin --tags
```

Also see ``github_release.py`` script to upload zip archive from CPack generator
to the release marked by tag. This prebuild files will use in building process.

2. Copy sources from original to borsch repository (don't copy build scripts).
One can use some diff utility to check changes (i.e. meld).
If ``opt/folders.csv`` exist use following command line utility:

```bash
python tools.py organize --src <path to sources> --dst_name <borsch repository name>
```

3. Check if everything build successfully

# Badge

Use special badge to mark repository supported NextGIS Borsch building system.

[![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch)

```md
[![Borsch compatible](https://img.shields.io/badge/Borsch-compatible-orange.svg?style=flat)](https://github.com/nextgis-borsch/borsch)
```

# License

All scripts are licensed under GNU GPL v.2.

# Notes

* There is additional util.cmake file for pretty print of version information to the console.
* MSVC 2015 and later have enough C99 support to build under Windows.

#Links:

* [FOSS4G 2016 Presentation (video)](https://ftp.gwdg.de/pub/misc/openstreetmap/FOSS4G-2016/foss4g-2016-1231-borsch_modern_build_system_for_c_c_gis_projects-hd.webm)
* [FOSS4G 2016 Presentation (slides)](http://nextgis.ru/wp-content/uploads/2016/08/NextGIS-Borsh-presentation.pdf)
