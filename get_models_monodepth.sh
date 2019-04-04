#!/bin/bash

MODELS=("kitti" "eigen" "cityscapes")
INSTALL_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

for MODEL in "${MODELS[@]}"
do
    URL="http://visual.cs.ucl.ac.uk/pubs/monoDepth/models/model_$MODEL.zip"
    OUTPUT_DIR="$INSTALL_SCRIPT_DIR/app/cnns/monodepth/models"
    OUTPUT_FILE="$OUTPUT_DIR/model_$MODEL.zip"
    echo -e "Downloading \033[0;32mmodel_${MODEL}.zip\033[0m in \033[0;32m${OUTPUT_DIR}\033[0m"
    wget -q -nc $URL -O $OUTPUT_FILE
    unzip $OUTPUT_FILE -d $OUTPUT_DIR
    rm $OUTPUT_FILE
done
