#!/usr/bin/env sh
DATA=./data_set

echo "Creating leveldb..."

rm -rf train_leveldb
rm -rf val_leveldb

convert_imageset \
    -shuffle \
    -backend leveldb \
    $DATA/train/ \
    $DATA/train.txt \
    train_leveldb 

convert_imageset \
    -shuffle \
    -backend leveldb \
    $DATA/val/ \
    $DATA/val.txt \
    val_leveldb 


echo "Done."
