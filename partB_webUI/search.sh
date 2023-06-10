#!/bin/bash
# This script is used to run part B of the project
read -e -p "Enter the path of the data folder: " DATA_PATH
if [ -d "./index" ]; then
    echo "Directory exists"
else
    mkdir index
fi
python3 indexer.py $DATA_PATH ./index
python3 app.py