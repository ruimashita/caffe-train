#!/usr/bin/env sh
DATA=./data_set

echo "Creating leveldb..."

rm -rf $DATA/train_leveldb
rm -rf $DATA/val_leveldb

convert_imageset \
    -shuffle \
    -backend leveldb \
    $DATA/train/ \
    $DATA/train.txt \
    $DATA/train_leveldb 

convert_imageset \
    -shuffle \
    -backend leveldb \
    $DATA/val/ \
    $DATA/val.txt \
    $DATA/val_leveldb 


echo "Done."
