#!/usr/bin/env sh
DATA=/home/docker/data_set

echo "Creating leveldb..."

rm -rf $DATA/train_leveldb
rm -rf $DATA/val_leveldb

convert_imageset \
    -shuffle \
    -backend leveldb \
    -resize_height 256 \
    -resize_width 256 \
    $DATA/train/ \
    $DATA/train.txt \
    $DATA/train_leveldb 

convert_imageset \
    -shuffle \
    -backend leveldb \
    -resize_height 256 \
    -resize_width 256 \
    $DATA/val/ \
    $DATA/val.txt \
    $DATA/val_leveldb 

# convert_imageset \
#     -shuffle \
#     -resize_height 256 \
#     -resize_width 256 \
#     $DATA/train/ \
#     $DATA/train.txt \
#     $DATA/train_leveldb 

# convert_imageset \
#     -shuffle \
#     -resize_height 256 \
#     -resize_width 256 \
#     $DATA/val/ \
#     $DATA/val.txt \
#     $DATA/val_leveldb 


echo "Done."
