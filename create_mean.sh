#!/usr/bin/env sh
DATA=./data_set

echo "Creating mean..."

if [ -e $DATA/train_leveldb ]; then
    echo "from leveldb"
    compute_image_mean -backend leveldb $DATA/train_leveldb mean.binaryproto
fi

if [ -e $DATA/train_lmdb ]; then
    echo "from lmdb"
    compute_image_mean $DATA/train_lmdb mean.binaryproto
fi

echo "Convert mean.binaryproto to mean.npy"

python convert_mean_proto_to_npy.py mean.binaryproto mean.npy

echo "Done."
