#!/usr/bin/env sh
DATA=./data_set
CONFIG_DIR=./config

echo "Creating mean..."

compute_image_mean -backend leveldb $DATA/train_leveldb $CONFIG_DIR/mean.binaryproto 
python convert_mean_proto_to_npy.py $DATA/mean.binaryproto $CONFIG_DIR/mean.npy

echo "Done."
