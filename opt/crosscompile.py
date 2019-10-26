#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Purpose: Android static builds
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Author: Maxim Dubinin <maim.dubinin@nextgis.com>
## Copyright (c) 2019 NextGIS <info@nextgis.com>
## License: GPL v.2
##
################################################################################

import argparse
import os
import time
import repka_release
import shutil
import subprocess
import common

ndk_path = '/Users/Bishop/Library/Android/sdk/ndk-bundle'
abis = ['x86_64', 'x86', 'arm64-v8a', 'armeabi-v7a']
base_opts = ['-DANDROID_TOOLCHAIN=clang', '-DANDROID_STL=c++_static', '-DANDROID_CPP_FEATURES=rtti', '-G', 'Unix Makefiles', '-DCMAKE_MAKE_PROGRAM=make', '-DBUILD_SHARED_LIBS=OFF', '-DBUILD_STATIC_LIBS=ON', '-DBUILD_TARGET_PLATFORM=ANDROID', '-DSUPPRESS_VERBOSE_OUTPUT=ON', '-DCMAKE_BUILD_TYPE=Release', '-DSKIP_DEFAULTS=ON', '-DCMAKE_TOOLCHAIN_FILE=' + ndk_path + '/build/cmake/android.toolchain.cmake', '-DANDROID_NDK=' + ndk_path]
repositories = [
    {"name": "lib_z", "args" : []},
    {"name": "lib_sqlite", "args" : ['-DBUILD_APP=OFF']},
    {"name": "lib_iconv", "args" : []},
    {"name": "lib_jsonc", "args" : []},
    {"name": "lib_jbig", "args" : []},
    {"name": "lib_expat", "args" : ['-DBUILD_tools=OFF', '-DBUILD_examples=OFF', '-DBUILD_tests=OFF', '-DBUILD_doc=OFF']},
    {"name": "lib_geos", "args" : ['-DGEOS_ENABLE_TESTS=OFF']},
    {"name": "lib_openssl", "args" : ['-DOPENSSL_NO_AFALGENG=ON', '-DOPENSSL_NO_ASM=ON', '-DOPENSSL_NO_DYNAMIC_ENGINE=ON', '-DOPENSSL_NO_STATIC_ENGINE=OFF', '-DOPENSSL_NO_DEPRECATED=ON', '-DOPENSSL_NO_UNIT_TEST=ON']},
    {"name": "lib_lzma", "args" : ['-DBUILD_APPS=OFF']},
    {"name": "lib_jpeg", "args" : ['-DBUILD_APP=OFF']},
    {"name": "lib_curl", "args" : ['-DWITH_OpenSSL_EXTERNAL=ON', '-DBUILD_CURL_EXE=OFF', '-DHTTP_ONLY=ON', '-DENABLE_MANUAL=OFF','-DWITH_ZLIB=ON', '-DCMAKE_USE_LIBSSH2=OFF', '-DCMAKE_USE_GSSAPI=OFF']},
    {"name": "lib_png", "args" : ['-DWITH_ZLIB=ON']},
    {"name": "lib_proj", "args" : ['-DBUILD_CCT=OFF', '-DBUILD_CS2CS=OFF', '-DBUILD_GEOD=OFF', '-DBUILD_GIE=OFF', '-DBUILD_PROJ=OFF', '-DBUILD_PROJINFO=OFF', '-DWITH_SQLite3=ON', '-DWITH_SQLite3_EXTERNAL=ON', '-DPROJ_TESTS=OFF', '-DGENERATE_PROJ_DB=OFF']},
    {"name": "lib_xml2", "args" : ['-DWITH_ZLIB=ON', '-DWITH_LibLZMA=ON', '-DWITH_LibLZMA_EXTERNAL=ON', '-DWITH_ICONV=ON', '-DWITH_ICONV_EXTERNAL=ON', '-DBUILD_TESTING=OFF']},
    {"name": "lib_tiff", "args" : ['-DWITH_ZLIB=ON', '-DWITH_JPEG_EXTERNAL=ON', '-DWITH_JBIG_EXTERNAL=ON', '-DWITH_LibLZMA_EXTERNAL=ON', '-DWITH_JPEG=ON', '-DWITH_JBIG=ON', '-DWITH_LibLZMA=ON', '-DSKIP_TOOLS=ON', '-DSKIP_BUILD_DOCS=ON']},
    {"name": "lib_geotiff", "args" : ['-DWITH_JPEG=ON', '-DWITH_JPEG_EXTERNAL=ON', '-DWITH_PROJ=ON', '-DWITH_PROJ_EXTERNAL=ON', '-DWITH_ZLIB=ON', '-DWITH_TIFF=ON', '-DWITH_TIFF_EXTERNAL=ON', '-DWITH_UTILITIES=OFF']},
    {"name": "lib_gdal", "args" : ['-DWITH_EXPAT=ON', '-DWITH_EXPAT_EXTERNAL=ON', '-DWITH_GeoTIFF=ON', '-DWITH_GeoTIFF_EXTERNAL=ON', '-DWITH_GEOS=ON', '-DWITH_GEOS_EXTERNAL=ON', '-DWITH_CURL=ON', '-DWITH_CURL_EXTERNAL=ON', '-DWITH_ICONV=ON', '-DWITH_ICONV_EXTERNAL=ON', '-DWITH_JBIG=ON', '-DWITH_JBIG_EXTERNAL=ON', '-DWITH_JPEG=ON', '-DWITH_JPEG_EXTERNAL=ON', '-DWITH_JPEG12=ON', '-DWITH_JPEG12_EXTERNAL=ON', '-DWITH_JSONC=ON', '-DWITH_JSONC_EXTERNAL=ON', '-DWITH_LibLZMA=ON', '-DWITH_LibLZMA_EXTERNAL=ON', '-DWITH_LibXml2=ON', '-DWITH_LibXml2_EXTERNAL=ON', '-DWITH_OpenSSL=ON', '-DWITH_OpenSSL_EXTERNAL=ON', '-DWITH_PNG=ON', '-DWITH_PNG_EXTERNAL=ON', '-DWITH_PROJ=ON', '-DWITH_PROJ_EXTERNAL=ON', '-DWITH_SQLite3=ON', '-DWITH_SQLite3_EXTERNAL=ON', '-DWITH_TIFF=ON', '-DWITH_TIFF_EXTERNAL=ON', '-DWITH_ZLIB=ON', '-DENABLE_MRF=OFF', '-DENABLE_PLSCENES=OFF', '-DENABLE_AAIGRID_GRASSASCIIGRID=OFF', '-DENABLE_ADRG_SRP=OFF', '-DENABLE_AIG=OFF', '-DENABLE_AIRSAR=OFF', '-DENABLE_ARG=OFF', '-DENABLE_BLX=OFF', '-DENABLE_BMP=OFF', '-DENABLE_BSB=OFF', '-DENABLE_CALS=OFF', '-DENABLE_CEOS=OFF', '-DENABLE_CEOS2=OFF', '-DENABLE_COASP=OFF', '-DENABLE_COSAR=OFF', '-DENABLE_CTG=OFF', '-DENABLE_DIMAP=OFF', '-DENABLE_DTED=OFF', '-DENABLE_E00GRID=OFF', '-DENABLE_EEDA=OFF', '-DENABLE_ELAS=OFF', '-DENABLE_ENVISAT=OFF', '-DENABLE_ERS=OFF', '-DENABLE_FIT=OFF', '-DENABLE_GFF=OFF', '-DENABLE_GIF=OFF', '-DENABLE_GRIB=OFF', '-DENABLE_GSAG_GSBG_GS7BG=OFF', '-DENABLE_GXF=OFF', '-DENABLE_HF2=OFF', '-DENABLE_IDRISI_RASTER=OFF', '-DENABLE_IGNFHeightASCIIGrid=OFF', '-DENABLE_ILWIS=OFF', '-DENABLE_INGR=OFF', '-DENABLE_IRIS=OFF', '-DENABLE_JAXAPALSAR=OFF', '-DENABLE_JDEM=OFF', '-DENABLE_KMLSUPEROVERLAY=OFF', '-DENABLE_L1B=OFF', '-DENABLE_LEVELLER=OFF', '-DENABLE_MAP=OFF', '-DENABLE_MBTILES=OFF', '-DENABLE_MSGN=OFF', '-DENABLE_NGSGEOID=OFF', '-DENABLE_NITF_RPFTOC_ECRGTOC=OFF', '-DENABLE_NWT=OFF', '-DENABLE_OZI=OFF', '-DENABLE_PCIDSK=OFF', '-DENABLE_PDS_ISIS2_ISIS3_VICAR=OFF', '-DENABLE_PLMOSAIC=OFF', '-DENABLE_POSTGISRASTER=OFF', '-DENABLE_PRF=OFF', '-DENABLE_R=OFF', '-DENABLE_RASTERLITE=OFF', '-DENABLE_RIK=OFF', '-DENABLE_RMF=OFF', '-DENABLE_RDA=OFF', '-DENABLE_RS2=OFF', '-DENABLE_SAFE=OFF', '-DENABLE_SAGA=OFF', '-DENABLE_SENTINEL2=OFF', '-DENABLE_SIGDEM=OFF', '-DENABLE_SDTS_RASTER=OFF', '-DENABLE_SGI=OFF', '-DENABLE_SRTMHGT=OFF', '-DENABLE_TERRAGEN=OFF', '-DENABLE_TIL=OFF', '-DENABLE_TSX=OFF', '-DENABLE_USGSDEM=OFF', '-DENABLE_WCS=OFF', '-DENABLE_WMTS=OFF', '-DENABLE_XPM=OFF', '-DENABLE_XYZ=OFF', '-DENABLE_ZMAP=OFF', '-DENABLE_AERONAVFAA=OFF', '-DENABLE_ARCGEN=OFF', '-DENABLE_AVC=OFF', '-DENABLE_BNA=OFF', '-DENABLE_CARTO=OFF', '-DENABLE_CLOUDANT=OFF', '-DENABLE_COUCHDB=OFF', '-DENABLE_CSV=OFF', '-DENABLE_CSW=OFF', '-DENABLE_DGN=OFF', '-DENABLE_DXF=OFF', '-DENABLE_EDIGEO=OFF', '-DENABLE_ELASTIC=OFF', '-DENABLE_GEOCONCEPT=OFF', '-DENABLE_GEORSS=OFF', '-DENABLE_GFT=OFF', '-DENABLE_GML=OFF', '-DENABLE_GMT=OFF', '-DENABLE_GPSBABEL=OFF', '-DENABLE_GTM=OFF', '-DENABLE_HTF=OFF', '-DENABLE_IDRISI_VECTOR=OFF', '-DENABLE_JML=OFF', '-DENABLE_NTF=OFF', '-DENABLE_ODS=OFF', '-DENABLE_OPENAIR=OFF', '-DENABLE_OPENFILEGDB=OFF', '-DENABLE_OSM=OFF', '-DENABLE_PDS_VECTOR=OFF', '-DENABLE_PG=OFF', '-DENABLE_PGDUMP=OFF', '-DENABLE_REC=OFF', '-DENABLE_S57=OFF', '-DENABLE_SDTS_VECTOR=OFF', '-DENABLE_SEGUKOOA=OFF', '-DENABLE_SEGY=OFF', '-DENABLE_SELAFIN=OFF', '-DENABLE_SUA=OFF', '-DENABLE_SVG=OFF', '-DENABLE_SXF=OFF', '-DENABLE_TIGER=OFF', '-DENABLE_VDV=OFF', '-DENABLE_VFK=OFF', '-DENABLE_WASP=OFF', '-DENABLE_WFS=OFF', '-DENABLE_XLSX=OFF', '-DENABLE_CAD=OFF', '-DGDAL_BUILD_APPS=OFF', '-DGDAL_BUILD_DOCS=OFF', '-DENABLE_NULL=OFF', '-DENABLE_NGW=ON', '-DENABLE_GNMFILE=OFF', '-DENABLE_ECW=OFF', '-DENABLE_GEORASTER=OFF', '-DENABLE_HDF4=OFF', '-DENABLE_MRSID=OFF', '-DENABLE_OPENJPEG=OFF', '-DENABLE_WEBP=OFF', '-DENABLE_LIBKML=OFF', '-DENABLE_MVT=OFF', '-DENABLE_OCI=OFF', '-DENABLE_RAW=OFF']},
    
]

def get_packages(package_list):
    out = []
    if package_list is not None:
        packagesList = package_list.split(';')
        for package in packagesList:
            for repo in repositories:
                if repo['name'] == package:
                    out.append(repo)
                    break
    else:
        out.extend(repositories)

    return out

def run(args):
    # print 'calling ' + string.join(args)
    try:
        output_code = subprocess.call(args, stderr=subprocess.STDOUT)
        return output_code == 0
    except subprocess.CalledProcessError, e:
        return False
    
def make_package(repo, root_dir, abi, login, password):
    common.color_print('Process {} [{}]...'.format(repo['name'], abi), False, 'LBLUE')
    repo_dir = os.path.join(root_dir, repo['name'])
    # Create build dir
    build_dir = os.path.join(root_dir, 'build', repo['name'] + '_' + str(int(time.time())))
    os.mkdir(build_dir)
    os.chdir(build_dir)

    # Configure
    run_args = ['cmake']
    run_args.extend(base_opts)
    run_args.append('-DANDROID_ABI=' + abi)
    run_args.extend(repo['args'])
    run_args.append(repo_dir)
    if run((run_args)) == False:
        exit('Failed to configure')

    # Make
    if run(('cmake', '--build', '.', '--config', 'Release', '--', '-j8')) == False:
        exit('Failed to make')

    # Pack
    if run(('cpack')) == False:
        exit('Failed to pack')

    # Send to repka
    repka_release.do_work(repo_dir, build_dir, login, password)

    # Delete dir
    shutil.rmtree(build_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NextGIS Borsch tools. Utility to create or recreate release in repository')
    parser.add_argument('-v', '--version', action='version', version='NextGIS Borsch repka_release version 1.0')
    parser.add_argument('--login', dest='login', help='repka login')
    parser.add_argument('--password', dest='password', help='repka password')
    parser.add_argument('--packages', dest='packages', help='packages list separated by semicolon')

    args = parser.parse_args()

    borsch_root_dir = os.path.join(os.getcwd(), os.pardir, os.pardir)
        
    for repo in get_packages(args.packages):
        for abi in abis:
            make_package(repo, borsch_root_dir, abi, args.login, args.password)