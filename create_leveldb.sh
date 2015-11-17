#!/usr/bin/env sh
DATA=./data_set

echo "Creating leveldb..."

rm -rf train_leveldb
rm -rf val_leveldb

GLOG_logtostderr=1 convert_imageset \
    -shuffle true \
    -backend leveldb \
    $DATA/train/ \
    $DATA/train.txt \
    $DATA/train_leveldb 

GLOG_logtostderr=1 convert_imageset \
    -shuffle true \
    -backend leveldb \
    $DATA/val/ \
    $DATA/val.txt \
    $DATA/val_leveldb 


echo "Done."
