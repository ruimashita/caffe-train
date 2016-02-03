# -*- coding: utf-8 -*-
import os
import sys
import glob
import random

import caffe
from caffe.proto import caffe_pb2
import lmdb
import numpy
import PIL.Image
import shutil

IMAGE_SIZE = 256
WORK_DIR = '/home/docker'

DATASET_DIR = WORK_DIR + '/data_set'
IMAGES_DIR = DATASET_DIR + '/images'
TRAIN_LMDB = DATASET_DIR +'/train_lmdb'
VAL_LMDB = DATASET_DIR + '/val_lmdb'
TRAIN_DATA = DATASET_DIR + '/train'
VAL_DATA = DATASET_DIR + '/val'


def reset_dir(dir_path):
    print "delete and make dir: {}".format(dir_path)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)

def reset_dirs():
    reset_dir(TRAIN_LMDB)
    reset_dir(VAL_LMDB)
    reset_dir(TRAIN_DATA)
    reset_dir(VAL_DATA)

def labels():
    dirs=[]
    for item in os.listdir(IMAGES_DIR):
        if os.path.isdir(os.path.join(IMAGES_DIR, item)):
            dirs.append(item)
    return dirs


def make_datum(image, label):

    return caffe_pb2.Datum(
        channels=3,
        width=IMAGE_SIZE,
        height=IMAGE_SIZE,
        label=label,
        data=numpy.rollaxis(numpy.asarray(image), 2).tostring()
    )



# label_map = {}
# train_filepaths = []
# val_filepaths = []

# train_male_filelists = glob.glob(TRAIN_DATA + '/male/*.jpg')

# train_female_filelists = glob.glob(TRAIN_DATA + '/female/*.jpg')

# ​

# for path in train_male_filelists: label_map[path] = 0

# for path in train_female_filelists: label_map[path] = 1

# ​

# train_filepaths.extend(train_male_filelists)

# train_filepaths.extend(train_female_filelists)

# ​

# val_male_filelists = glob.glob(val_data + '/male/*.jpg')

# val_female_filelists = glob.glob(val_data + '/female/*.jpg')

# ​

# for path in val_male_filelists: label_map[path] = 0

# for path in val_female_filelists: label_map[path] = 1

# ​

# val_filepaths.extend(val_male_filelists)

# val_filepaths.extend(val_female_filelists)

# ​

# random.shuffle(train_filepaths)

# random.shuffle(val_filepaths)

# ​

# print 'train'

# ​

# in_db = lmdb.open(train_lmdb, map_size=int(1e12))

# with in_db.begin(write=True) as in_txt:

#     for i, filename in enumerate(train_filepaths):

#         image = PIL.Image.open(filename)

#         datum = make_datum(image, label_map[filename])

#         in_txt.put('{:0>5d}'.format(i), datum.SerializeToString())

#         print '{:0>5d}'.format(i) + ':' + filename

# in_db.close()

# ​

# print 'val'

# in_db = lmdb.open(val_lmdb, map_size=int(1e12))

# with in_db.begin(write=True) as in_txt:

#     for i, filename in enumerate(val_filepaths):

#         image = PIL.Image.open(filename)

#         datum = make_datum(image, label_map[filename])

#         in_txt.put('{:0>5d}'.format(i), datum.SerializeToString())

#         print '{:0>5d}'.format(i) + ':' + filename

# in_db.close()


if __name__ == "__main__":
    print labels()
