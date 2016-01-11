#!/usr/bin/env sh
DATA=./data_set

echo "Creating lmdb."

rm -rf $DATA/train_lmdb
rm -rf $DATA/val_lmdb

convert_imageset \
    -shuffle \
    -resize_height 256 \
    -resize_width 256 \
    $DATA/train/ \
    $DATA/train.txt \
    $DATA/train_lmdb 

convert_imageset \
    -shuffle \
    -resize_height 256 \
    -resize_width 256 \
    $DATA/val/ \
    $DATA/val.txt \
    $DATA/val_lmdb 


echo "Done."
