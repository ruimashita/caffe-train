#!/usr/bin/env sh
DATA=./data_set

echo "Creating mean..."

compute_image_mean -backend leveldb $DATA/train_leveldb mean.binaryproto 
python convert_mean_proto_to_npy.py mean.binaryproto mean.npy

echo "Done."
