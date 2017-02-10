# Introduction
Many C/C++ GIS libraries are usually built via autoconf/make/nmake/VC. While this is valid approach, we believe there is a better new alternative - CMake. NextGIS Borsch (http://nextgis.com/borsch) is a new build system that is a) easier to use, b) better solves dependencies and c) provides more uniform way of building packages. Needed dependencies are automatically fetched from repositories. We’ve built an early prototype of such system and tested if on GDAL build process (over 50 core dependent libraries). Now a developer with only three lines of code in CMakeLists.txt for any project he is working on can add dependent GIS library. If needed library exists in the system the build system will use it, if not - it will be downloaded from Github. Our new build system works for both Windows and Linux.

# Common CMake scripts
These are common cmake scripts for building system.
Now two main files created **FindAnyProject.cmake** and **FindExtProject.cmake**.

FindAnyProject.cmake - have two main functions: find_anyproject and target_link_extlibraries.

The first one tries to find_package locally. If no package found user can opt to use external project. The FindExtProject.cmake is used for this.

The second one is used to link target libraries from both local or external packages.

Finally, there are sets of FindExtxxx.cmake files for external repositories details and additional logic.

# Use cases

To use this scripts one have to add cmake folder to the sources.
Than the folder needs to be added to modules path:

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

Version can be specified via VERSION ```<version>```

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

| # | Repository | Cmaked  | OS tested | Notes |
|:-:|---|:-:|---|:---|
|1| [lib_z](https://github.com/nextgis-borsch/lib_z)  | yes | Linux, Windows | tests present, not needed on Mac OS |
|2| [lib_lzma](https://github.com/nextgis-borsch/lib_lzma) | yes | Linux, Windows, Mac OS X |  |
|3| [lib_xml2](https://github.com/nextgis-borsch/lib_xml2) | yes | Linux, Windows | not needed on Mac OS |
|4| [lib_curl](https://github.com/nextgis-borsch/lib_curl) | yes | Linux, Windows, Mac OS X | |
|5| [lib_geotiff](https://github.com/nextgis-borsch/lib_geotiff) | yes | Linux, Windows, Mac OS X |  |
|6| [lib_tiff](https://github.com/nextgis-borsch/lib_tiff) | yes | Linux, Windows, Mac OS X |  |
|7| [lib_jpeg](https://github.com/nextgis-borsch/lib_jpeg) | yes | Linux, Windows, Mac OS X |  |
|8| [lib_jbig](https://github.com/nextgis-borsch/lib_jbig) | yes | Linux, Windows, Mac OS X |  |
|9| [lib_iconv](https://github.com/nextgis-borsch/lib_iconv) | yes | Linux, Windows | not needed on Mac OS |
|10| [lib_gdal](https://github.com/nextgis-borsch/lib_gdal) | yes | Linux, Windows, Mac OS X | tests present |
|11| [lib_openssl](https://github.com/nextgis-borsch/lib_openssl) | yes | Linux, Windows, Mac OS X |  |
|12| [lib_jsonc](https://github.com/nextgis-borsch/lib_jsonc) | yes | Linux, Windows, Mac OS X | tests present |
|13| [lib_expat](https://github.com/nextgis-borsch/lib_expat) | yes | Linux, Windows | tests present, not needed on Mac OS |
|14| [lib_proj](https://github.com/nextgis-borsch/lib_proj) | yes | Linux, Windows, Mac OS X |  |
|15| [lib_png](https://github.com/nextgis-borsch/lib_png) | yes | Linux, Windows, Mac OS X | tests present |
|16| [lib_hdf4](https://github.com/nextgis-borsch/lib_hdf4) | yes | Linux, Windows |  |
|17| lib_hdf5 | no |  | For GDAL Hierarchical Data Format Release 5 (HDF5) driver |
|18| [lib_szip](https://github.com/nextgis-borsch/lib_szip) | yes | Linux, Windows | tests present |
|19| [lib_hdfeos2](https://github.com/nextgis-borsch/lib_hdfeos2) | yes | Linux, Windows | tests present, 7 failed |
|20| [lib_geos](https://github.com/nextgis-borsch/lib_geos) | yes | Linux, Windows, Mac OS X |  |
|21| lib_hdfeos5 | no | |  |
|22| lib_bpg | no | | For GDAL BPG (Better Portable Graphics) driver |
|23| lib_dap | no | | For GDAL DODS / OPeNDAP driver |
|24| lib_epsilon | no | | For GDAL Epsilon - Wavelet compressed images driver |
|25| lib_cfitsio | no | | For GDAL FITS (.fits) driver |
|26| [lib_sqlite3](https://github.com/nextgis-borsch/lib_sqlite) | yes | Linux, Windows, Mac OS X | For GDAL GeoPackage and other drivers |
|27| lib_gif | no | | For GDAL GIF driver |
|28| lib_netcdf | no | | For GDAL GMT Compatible netCDF driver |
|29| lib_grass | no | | For GDAL GRASS driver |
|30| lib_gta | no | | For GDAL Generic Tagged Arrays (.gta) driver |
|31| lib_jasper | no | | For GDAL JPEG2000 (.jp2, .j2k) driver |
|32| lib_openjpeg | no | | For GDAL OpenJPEG driver |
|33| lib_csf | no | | For GDAL PCRaster driver |
|34| lib_pdfium | no | | For GDAL Geospatial PDF driver |
|35| [lib_pq](https://github.com/nextgis-borsch/lib_pq) | yes | Linux, Windows, Mac OS X | For GDAL PostGIS Raster driver. [libpq CMakeLists.txt]( https://github.com/stalkerg/postgres_cmake/blob/cmake/src/interfaces/libpq/CMakeLists.txt)|
|36| lib_ras | no | | For GDAL Rasdaman driver |
|37| lib_webp | no | | For GDAL WEBP driver |
|38| lib_xerces | no | | For GDAL INTERLIS driver |
|39| lib_kml | no | | For GDAL LIBKML driver |
|40| lib_mongo | no | | For GDAL MongoDB driver |
|41| lib_mysql | no | | For GDAL MySQL driver |
|42| lib_pcidsk | no | | For GDAL PCI Geomatics Database File driver |
|43| lib_podofo | no | | For GDAL Geospatial PDF driver |
|44| [lib_freexl](https://github.com/nextgis-borsch/lib_freexl) | yes | Windows | For GDAL MS Excel format driver |
|45| [lib_spatialite](https://github.com/nextgis-borsch/lib_spatialite) | yes | Windows | For GDAL spatialite/sqlite format driver |
|46| [lib_spatialindex](https://github.com/nextgis-borsch/lib_spatialindex) | yes | Windows | |
|47| [googletest](https://github.com/nextgis-borsch/googletest) | yes | Linux, Mac OS X | |
|48| [lib_boost](https://github.com/nextgis-borsch/lib_boost) | yes | | Make only copies of headers from "boost/" without building libs |
|49| [lib_zip](https://github.com/nextgis-borsch/lib_zip) | yes | | |
|50| [lib_uv](https://github.com/nextgis-borsch/lib_uv) | yes | | |
|51| [lib_jpegturbo](https://github.com/nextgis-borsch/lib_jpegturbo) | no | | |
|52| [lib_variant](https://github.com/nextgis-borsch/lib_variant) | yes | | |
|53| [lib_rapidjson](https://github.com/nextgis-borsch/lib_rapidjson) | yes | | |
|54| [lib_nunicode](https://github.com/nextgis-borsch/lib_nunicode) | yes | | cmaked within the requirements of the mapbox |
|55| [lib_geojsonvt](https://github.com/nextgis-borsch/lib_geojsonvt) | yes | | |
|56| [postgis](https://github.com/nextgis-borsch/postgis) | yes | Linux | partially cmaked (except tiger and cgal) |
|57| [lib_opencad](https://github.com/nextgis-borsch/lib_opencad) | yes | Linux | From GSoC2016 |
|58| [numpy](https://github.com/nextgis-borsch/numpy) | yes | Mac OS X | Not a package but used for python dependency modules |
|59| [lib_ecw](https://github.com/nextgis-borsch/lib_ecw) | yes | Windows | Prebuild libraries for specific compiler and OS |
|60| [lib_mrsid](https://github.com/nextgis-borsch/lib_mrsid) | yes | Windows | Prebuild libraries for specific compiler and OS |
|61| [lib_gsl](https://github.com/nextgis-borsch/lib_gsl) | yes | Mac OS X | |
|62| [lib_qt4](https://github.com/nextgis-borsch/lib_qt4) | yes | Mac OS X | Sources received from Qt download site and build using their own build system |
|63| [lib_qt5](https://github.com/nextgis-borsch/lib_qt5) | | | |
|64| [lib_qca](https://github.com/nextgis-borsch/lib_qca) | yes | Mac OS X |  |
|65| [lib_qwt](https://github.com/nextgis-borsch/lib_qwt) | yes | Mac OS X |  |
|66| [lib_qscintilla](https://github.com/nextgis-borsch/lib_qca) | yes | Mac OS X |  |
|67| [lib_cgal](https://github.com/nextgis-borsch/lib_cgal) | yes | | |
|68| [py_qt4](https://github.com/nextgis-borsch/py_qt4) | yes | Mac OS X | Sources received from Riverbank download site and build using their own build system |
|69| [py_sip](https://github.com/nextgis-borsch/py_sip) | yes | Mac OS X | Sources received from Riverbank download site and build using their own build system |
|70| [tests](https://github.com/nextgis-borsch/tests) | | | |

# CMaked libraries requirements  

1. Make install instructions according to the GNU standard installation directories. Use include(GNUInstallDirs). For Mac OS X use option key OSX_FRAMEWORK=ON. Installation directories should be for frameworks: ```<CMAKE_INSTALL_PREFIX>/Library/Frameworks/<lib name in lower case without lib prefix>.framework``` and for applications:
```<CMAKE_INSTALL_PREFIX>/Applications/<app name>.app```
2. Add export instruction:

   ```cmake
   export(TARGETS ${EXPORT_TARGETS} FILE ${EXPORT_NAME}-exports.cmake EXPORT_LINK_INTERFACE_LIBRARIES)
   ```
3. All dependencies must be connected via find_anyproject (see "Borsch scripts").  
3.1. You need to add the relevant scripts from borsch to 'cmake' directory  
3.2. Add cmake instruction (if it is not present):

   ```cmake
   set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
   ```
4. Preferably cmake via include(util) should extract version from header file or another files and report it colored
5. Preferably add Findxxx.cmake with version check (see. [FindGEOS](https://github.com/nextgis-borsch/borsch/blob/master/cmake/FindGEOS.cmake) and [FindPROJ4](https://github.com/nextgis-borsch/borsch/blob/master/cmake/FindPROJ4.cmake))
6. Create FindExtxxx.cmake with library repository name and some optional variables
7. Add REGISTER_PACKAGE block to register libraries in CMake global repository on target system.

# Update library sources
Then new version of a library released, borsch need to be updated too.

1. Create tag for current version in repository and send it to server:

  ```bash
  git tag -a v1.0.2 -m 'version 1.0.2a from 22 Jan 2015'
  git push origin --tags
  ```

2. Copy sources from original to borsch repository (don't copy build scripts).
One can use some diff utility to check changes (i.e. meld).

3. Check if everything build successfully

# License

All scripts are licensed under GNU GPL v.2.

# Notes

* There is additional util.cmake file for pretty print of version information to the console.
* MSVC 2013 update 2 and later have enough C99 support to build under Windows.

#Links:

* [FOSS4G 2016 Presentation (video)](https://ftp.gwdg.de/pub/misc/openstreetmap/FOSS4G-2016/foss4g-2016-1231-borsch_modern_build_system_for_c_c_gis_projects-hd.webm)
* [FOSS4G 2016 Presentation (slides)](http://nextgis.ru/wp-content/uploads/2016/08/GDAL-2.1-FOSS4G-Bonn-2016.pdf)
