#!/bin/bash
set -xe

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}"

if [ ! -d "data" ]; then
    mkdir -p "data"
fi

URLBASE="http://www.wim.uni-mannheim.de/fileadmin/lehrstuehle/pi4/content/projects/retargeting/test_sequences-videos_for_table/"

curl -L -o data/news.mp4 "${URLBASE}/news_CIF.mp4"
curl -L -o data/ice.mp4 "${URLBASE}/ice_CIF.mp4"
