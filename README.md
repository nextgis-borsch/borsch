# Introduction
Many C/C++ GIS libraries are usually built via autoconf/make/nmake/VC. While this is valid approach, we believe there is a better new alternative - CMake. Enter NextGIS Borsch (http://nextgis.ru/en/borsch) - new build system that is a) easier to use, b) better solves depencies and c) provides more uniform way of building packages. Needed dependencies are automatically fetched from repositories. We’ve built an early prototype of such system and tested if on GDAL build process (over 50 core dependent libraries). Now a developer with only three lines of code in CMakeLists.txt for any project he is working on can add dependent GIS library. If needed library exists in the system the build system will use it, if not - it will be downloaded from Github. Our new build system works for both Windows and Linux.

# Common cmake scripts
This is common cmake scripts for building system. 
Now two main files created **FindAnyProject.cmake** and **FindExtProject.cmake**.

FindAnyProject.cmake - have two main functions: find_anyproject and target_link_extlibraries. 

The first one try to find_package locally. If no package found user can select to use external project. The FindExtProject.cmake used for it.

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
include(FindAnyProject)

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

Any other parameters will be forward to the external project. The important parameter is **CMAKE_ARGS**. Note: do not pass WITH_X options with CMAKE_ARGS, use set(WITH_X ...) instead.

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
|---|:-:|---|:---|
| [lib_z](https://github.com/nextgis-extra/lib_z)  | yes | Linux, Windows | tests present |
| [lib_lzma](https://github.com/nextgis-extra/lib_lzma) | yes | Linux, Windows |  |
| [lib_xml2](https://github.com/nextgis-extra/lib_xml2) | yes | Linux, Windows |  |
| [lib_curl](https://github.com/nextgis-extra/lib_curl) | yes | Windows |  |
| [lib_geotiff](https://github.com/nextgis-extra/lib_geotiff) | yes | Linux, Windows |  |
| [lib_tiff](https://github.com/nextgis-extra/lib_tiff) | yes | Linux, Windows |  |
| [lib_jpeg](https://github.com/nextgis-extra/lib_jpeg) | yes | Linux, Windows |  |
| [lib_jbig](https://github.com/nextgis-extra/lib_jbig) | yes | Linux, Windows |  |
| [lib_iconv](https://github.com/nextgis-extra/lib_iconv) | yes | Linux, Windows |  |
| [lib_gdal](https://github.com/nextgis-extra/lib_gdal) | yes | Linux, Windows | tests present |
| [lib_openssl](https://github.com/nextgis-extra/lib_openssl) | yes | Windows |  |
| [lib_jsonc](https://github.com/nextgis-extra/lib_jsonc) | yes | Linux, Windows | tests present |
| [lib_expat](https://github.com/nextgis-extra/lib_expat) | yes | Linux, Windows | tests present |
| [lib_proj](https://github.com/nextgis-extra/lib_proj) | yes | Linux, Windows |  |
| [lib_png](https://github.com/nextgis-extra/lib_png) | yes | Linux, Windows | tests present |
| [lib_hdf4](https://github.com/nextgis-extra/lib_hdf4) | yes | Linux, Windows |  |
| lib_hdf5 | no |  | For GDAL Hierarchical Data Format Release 5 (HDF5) driver |
| [lib_szip](https://github.com/nextgis-extra/lib_szip) | yes | Linux, Windows | tests present |
| [lib_hdfeos2](https://github.com/nextgis-extra/lib_hdfeos2) | yes | Linux, Windows | tests present |
| [lib_geos](https://github.com/nextgis-extra/lib_geos) | yes | Linux, Windows |  |
| lib_hdfeos5 | no | |  |
| lib_bpg | no | | For GDAL BPG (Better Portable Graphics) driver |
| lib_dap | no | | For GDAL DODS / OPeNDAP driver |
| lib_epsilon | no | | For GDAL Epsilon - Wavelet compressed images driver |
| lib_cfitsio | no | | For GDAL FITS (.fits) driver |
| [lib_sqlite3](https://github.com/nextgis-extra/lib_sqlite) | yes | Windows | For GDAL GeoPackage and other drivers |
| lib_gif | no | | For GDAL GIF driver |
| lib_netcdf | no | | For GDAL GMT Compatible netCDF driver |
| lib_grass | no | | For GDAL GRASS driver |
| lib_gta | no | | For GDAL Generic Tagged Arrays (.gta) driver |
| lib_jasper | no | | For GDAL JPEG2000 (.jp2, .j2k) driver |
| lib_openjpeg | no | | For GDAL OpenJPEG driver |
| lib_csf | no | | For GDAL PCRaster driver |
| lib_pdfium | no | | For GDAL Geospatial PDF driver |
| [lib_pq](https://github.com/nextgis-extra/lib_pq) | no | | For GDAL PostGIS Raster driver. [libpq CMakeLists.txt]( https://github.com/stalkerg/postgres_cmake/blob/cmake/src/interfaces/libpq/CMakeLists.txt)|
| lib_ras | no | | For GDAL Rasdaman driver |
| lib_webp | no | | For GDAL WEBP driver |
| lib_xerces | no | | For GDAL INTERLIS driver |
| lib_kml | no | | For GDAL LIBKML driver |
| lib_mongo | no | | For GDAL MongoDB driver |
| lib_mysql | no | | For GDAL MySQL driver |
| lib_pcidsk | no | | For GDAL PCI Geomatics Database File driver |
| lib_podofo | no | | For GDAL Geospatial PDF driver |
| [lib_freexl](https://github.com/nextgis-extra/lib_freexl) | yes | Windows | For GDAL MS Excel format driver |
| [lib_spatialite](https://github.com/nextgis-extra/lib_spatialite) | yes | Windows | For GDAL spatialite/sqlite format driver |
| [lib_spatialiteindex](https://github.com/nextgis-extra/lib_spatialiteindex) | yes | Windows | |

# Cmaked libraries requirements  
1. Make install instructions according to the GNU standard installation directories. Use include(GNUInstallDirs)  
2. Add export instruction:  
export(TARGETS ${EXPORT_TARGETS} FILE ${EXPORT_NAME}-exports.cmake EXPORT_LINK_INTERFACE_LIBRARIES)  
3. All dependencies must be connected via find_anyproject (see "Common cmake scripts").  
3.1. You need to add the relevant scripts from common_cmake to 'cmake' directory  
3.2. Add cmake instruction (if it is not present):  
SET(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})  
4. Preferably cmake via include(util) should extract version from header file or another files and report it colored
5. Preferably add Findxxx.cmake with version check (see. [FindGEOS](https://github.com/nextgis-extra/common_cmake/blob/master/cmake/FindGEOS.cmake) and [FindPROJ4](https://github.com/nextgis-extra/common_cmake/blob/master/cmake/FindPROJ4.cmake))
6. Create FindExtxxx.cmake with library repository name and some optional variables

# License

All scripts are licensed under GNU GPL v.2. 

# Notes

* There is additional util.cmake file for pretty print of version information to the console. 

* MSVC 2013 update 2 and later have enough C99 support to build under Windows.
