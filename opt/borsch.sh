#!/bin/bash

# Дополнительные свойства для текта:
BOLD='\033[1m'       #  ${BOLD}      # жирный шрифт (интенсивный цвет)
DBOLD='\033[2m'      #  ${DBOLD}    # полу яркий цвет (тёмно-серый, независимо от цвета)
NBOLD='\033[22m'      #  ${NBOLD}    # установить нормальную интенсивность
UNDERLINE='\033[4m'     #  ${UNDERLINE}  # подчеркивание
NUNDERLINE='\033[4m'     #  ${NUNDERLINE}  # отменить подчеркивание
BLINK='\033[5m'       #  ${BLINK}    # мигающий
NBLINK='\033[5m'       #  ${NBLINK}    # отменить мигание
INVERSE='\033[7m'     #  ${INVERSE}    # реверсия (знаки приобретают цвет фона, а фон -- цвет знаков)
NINVERSE='\033[7m'     #  ${NINVERSE}    # отменить реверсию
BREAK='\033[m'       #  ${BREAK}    # все атрибуты по умолчанию
NORMAL='\033[0m'      #  ${NORMAL}    # все атрибуты по умолчанию

# Цвет текста:
BLACK='\033[0;30m'     #  ${BLACK}    # чёрный цвет знаков
RED='\033[0;31m'       #  ${RED}      # красный цвет знаков
GREEN='\033[0;32m'     #  ${GREEN}    # зелёный цвет знаков
YELLOW='\033[0;33m'     #  ${YELLOW}    # желтый цвет знаков
BLUE='\033[0;34m'       #  ${BLUE}      # синий цвет знаков
MAGENTA='\033[0;35m'     #  ${MAGENTA}    # фиолетовый цвет знаков
CYAN='\033[0;36m'       #  ${CYAN}      # цвет морской волны знаков
GRAY='\033[0;37m'       #  ${GRAY}      # серый цвет знаков

# Цвет текста (жирным) (bold) :
DEF='\033[0;39m'       #  ${DEF}
DGRAY='\033[1;30m'     #  ${DGRAY}
LRED='\033[1;31m'       #  ${LRED}
LGREEN='\033[1;32m'     #  ${LGREEN}
LYELLOW='\033[1;33m'     #  ${LYELLOW}
LBLUE='\033[1;34m'     #  ${LBLUE}
LMAGENTA='\033[1;35m'   #  ${LMAGENTA}
LCYAN='\033[1;36m'     #  ${LCYAN}
WHITE='\033[1;37m'     #  ${WHITE}

# Цвет фона
BGBLACK='\033[40m'     #  ${BGBLACK}
BGRED='\033[41m'       #  ${BGRED}
BGGREEN='\033[42m'     #  ${BGGREEN}
BGBROWN='\033[43m'     #  ${BGBROWN}
BGBLUE='\033[44m'     #  ${BGBLUE}
BGMAGENTA='\033[45m'     #  ${BGMAGENTA}
BGCYAN='\033[46m'     #  ${BGCYAN}
BGGRAY='\033[47m'     #  ${BGGRAY}
BGDEF='\033[49m'      #  ${BGDEF}


DIR_NONE="!_NONE_!"
ALL_IS_OK_MSG="${BOLD}${BGDEF}${LMAGENTA} All is OK ${NORMAL}"

git_clone() {
    echo -e "${BOLD}${BGDEF}${LCYAN} clone $1 ${NORMAL}"
    repo="git@github.com:nextgis-borsch/$1.git"
    git clone $repo && echo -e "${ALL_IS_OK_MSG}"
}


git_addall() {
    echo -e "${BOLD}${BGDEF}${LCYAN} add all changes in $1 ${NORMAL}"
    cd $1
    git add -A && echo -e "${ALL_IS_OK_MSG}"
    cd ..
}


git_commit() {
    echo -e "${BOLD}${BGDEF}${LCYAN} commit "$2" in $1 ${NORMAL}"
    cd $1
    git commit -m "$2" && echo -e "${ALL_IS_OK_MSG}"
    cd ..
}


git_send() {
    echo -e "${BOLD}${BGDEF}${LCYAN} push $1 ${NORMAL}"
    cd $1
    git add . && git commit -a -m "$2" && git push && echo -e "${ALL_IS_OK_MSG}"
    cd ..
}

git_push() {
    echo -e "${BOLD}${BGDEF}${LCYAN} push $1 ${NORMAL}"
    cd $1
    git push && echo -e "${ALL_IS_OK_MSG}"
    cd ..
}

git_pull() {
    echo -e "${BOLD}${BGDEF}${LYELLOW} pull $1 ${NORMAL}"
    cd $1
    git pull && echo -e "${ALL_IS_OK_MSG}"
    cd ..
}


git_status() {
    echo -e "${BOLD}${BGDEF}${LGREEN} status $1 ${NORMAL}"
    cd $1
    git status
    cd ..
}


git_diff() {
    echo -e "${BOLD}${BGDEF}${LGREEN} diff $1 ${NORMAL}"
    cd $1
    git diff
    cd ..
}


git_lastlog() {
    echo -e "${BOLD}${BGDEF}${LGREEN} last log header for $1 ${NORMAL}"
    cd $1
    git log -1
    cd ..
}


repo_cmd() {
    CMDR="$1"
    REPO=$2
    REPO_DIR=$3

    echo -e "${BOLD}${BGDEF}${LGREEN} perform cmd ${CMDR} for ${REPO} ${NORMAL}"
    cd ${REPO}
    ${CMDR} && echo -e "${ALL_IS_OK_MSG}"
    cd ..
}


repo_copy() {
    SRC_FILE=$1
    REPO=$2
    REPO_DIR=$3

    echo -e "${BOLD}${BGDEF}${LGREEN} copy ${SRC_FILE} to ${REPO} ${NORMAL}"

    DST_DIR="cmake"

    if [[ ${REPO_DIR} != "" ]]
    then
        DST_DIR=${REPO_DIR}
    fi

    if [[ ${REPO_DIR} != ${DIR_NONE} ]]
    then
        cp -v ./borsch/cmake/${SRC_FILE} ./${REPO}/${DST_DIR}/${SRC_FILE}
    else
        echo -e "${BOLD}${BGDEF}${LYELLOW} Cmake dir does not exist ${NORMAL}"
    fi
}


repo_update() {
    SRC_FILE=$1
    REPO=$2
    REPO_DIR=$3

    echo -e "${BOLD}${BGDEF}${LGREEN} update ${SRC_FILE} if exist in ${REPO} ${NORMAL}"

    DST_DIR="cmake"

    if [[ ${REPO_DIR} != "" ]]
    then
        DST_DIR=${REPO_DIR}
    fi

    SRC_FILE_PATH=./borsch/cmake/${SRC_FILE}
    DST_FILE_PATH=./${REPO}/${DST_DIR}/${SRC_FILE}

    if [[ -f ${DST_FILE_PATH} ]]
    then
        cp -v ${SRC_FILE_PATH} ${DST_FILE_PATH}
    else
        echo -e "${BOLD}${BGDEF}${LYELLOW} File ${SRC_FILE} does not exist, do not update it ${NORMAL}"
    fi
}


repo_delete() {
    SRC_FILE=$1
    REPO=$2
    REPO_DIR=$3

    echo -e "${BOLD}${BGDEF}${LGREEN} delete ${SRC_FILE} in ${REPO} ${NORMAL}"

    DST_DIR="cmake"

    if [[ ${REPO_DIR} != "" ]]
    then
        DST_DIR=${REPO_DIR}
    fi

    DST_FILE_PATH=./${REPO}/${DST_DIR}/${SRC_FILE}

    if [[ -f ${DST_FILE_PATH} ]]
    then
        rm -v -i ${DST_FILE_PATH}
    else
        echo -e "${BOLD}${BGDEF}${LYELLOW} File ${SRC_FILE} does not exist ${NORMAL}"
    fi
}


repos=(
 "borsch"
 "lib_curl"
 "lib_openssl"
 "lib_tiff"
 "lib_lzma"
 "lib_hdf4"
 "lib_png"
 "lib_geotiff"
 "tests"
 "lib_xml2"
 "lib_hdfeos2"
 "lib_gdal"
 "lib_pq"
 "lib_spatialite"
 "lib_iconv"
 "lib_freexl"
 "lib_spatialindex"
 "postgis"
 "lib_geos"
 "lib_sqlite"
 "lib_proj"
 "lib_jsonc"
 "lib_szip"
 "lib_jpeg"
 "lib_z"
 "lib_jbig"
 "lib_expat"
 "googletest"
 "lib_boost"
 "lib_zip"
 "lib_uv"
 "lib_jpegturbo"
 "lib_variant"
 "lib_rapidjson"
 "lib_nunicode"
 "lib_geojsonvt"
 "lib_opencad"
 "lib_ecw"
 "lib_mrsid"
)


declare -A cmake_dirs=(
    ["lib_curl"]="CMake"
    ["lib_spatialindex"]=${DIR_NONE}
)


case "$1" in
        clone)
            cd ../..
            for repo in ${repos[@]}
            do
                git_clone "$repo"
            done
            ;;

        addall)
            cd ../..
            for repo in ${repos[@]}
            do
                git_addall "$repo"
            done
            ;;

        commit)
            cd ../..
            for repo in ${repos[@]}
            do
                git_commit "$repo" "$2"
            done
            ;;

        send)
            cd ../..
            for repo in ${repos[@]}
            do
                git_send "$repo" "$2"
            done
            ;;

	push)
	    cd ../..
	    for repo in ${repos[@]}
	    do
		git_push "$repo"
	    done
	    ;;

        pull)
            cd ../..
            for repo in ${repos[@]}
            do
                git_pull "$repo"
            done
            ;;

        status)
            cd ../..
            for repo in ${repos[@]}
            do
                git_status "$repo"
            done
            ;;

        diff)
            cd ../..
            for repo in ${repos[@]}
            do
                git_diff "$repo"
            done
            ;;

        lastlog)
            cd ../..
            for repo in ${repos[@]}
            do
                git_lastlog "$repo"
            done
            ;;

        cmd)
            cd ../..
            for repo in ${repos[@]}
            do
                repo_cmd "$2" "$repo" "${cmake_dirs[${repo}]}"
            done
            ;;

        copy)
            cd ../..
            for repo in ${repos[@]}
            do
                repo_copy $2 "$repo" "${cmake_dirs[${repo}]}"
            done
            ;;

        update)
            cd ../..
            for repo in ${repos[@]}
            do
                repo_update $2 "$repo" "${cmake_dirs[${repo}]}"
            done
            ;;

        delete)
            cd ../..
            for repo in ${repos[@]}
            do
                repo_delete $2 "$repo" "${cmake_dirs[${repo}]}"
            done
            ;;

        *)
            echo $"Usage: $0 {clone|addall|commit|send|push|pull|status|diff|cmd|lastlog|copy|update|delete}"
            exit 1

esac
