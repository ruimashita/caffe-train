# -*- coding: utf-8 -*-
import csv
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
TRAIN_DIR = DATASET_DIR + '/train'
VAL_DIR = DATASET_DIR + '/val'
LABELS_CSV_FILE = WORK_DIR + '/data_set/labels.csv'

SPLIT_VAL_RATE = 3  #

def reset_dir(dir_path):
    print "delete and make dir: {}".format(dir_path)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)

def reset_dirs():
    reset_dir(TRAIN_LMDB)
    reset_dir(VAL_LMDB)
    reset_dir(TRAIN_DIR)
    reset_dir(VAL_DIR)

    for label_name in labels():
        train_dir = '{0}/{1}'.format(TRAIN_DIR, label_name)
        val_dir = '{0}/{1}'.format(VAL_DIR, label_name)

        reset_dir(train_dir)
        reset_dir(val_dir)

def labels():
    dirs = []
    for item in os.listdir(IMAGES_DIR):
        if os.path.isdir(os.path.join(IMAGES_DIR, item)):
            dirs.append(item)
    dirs.sort()
    return dirs


def write_labels_csv_file():

    with open(LABELS_CSV_FILE, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)

        for i, label in enumerate(labels()):
             writer.writerow([i, label])


def get_label_name(path):
    return os.path.basename(os.path.dirname(path))


def get_label_index(path):
    return labels().index(get_label_name(path))


def split_train_val():
    reset_dirs()

    paths = glob.glob(IMAGES_DIR + '/*/*.jpg')
    paths.sort()

    print 'exec split train val. all images num: {}'.format(len(paths))

    for path in paths:
        rand = random.randint(1, 10)
        label_name = get_label_name(path)
        if rand <= SPLIT_VAL_RATE:
            print 'split to val: {}'.format(path)
            dir_name = '{0}/{1}'.format(VAL_DIR, label_name)
        else:
            print 'split to train: {}'.format(path)
            dir_name = '{0}/{1}'.format(TRAIN_DIR, label_name)
        shutil.copy(path, dir_name)

def make_lmdb(db_path, paths):
    print 'create db: {0}'.format(db_path)

    os.system('rm -rf ' + db_path)
    random.shuffle(paths)

    in_db = lmdb.open(db_path, map_size=int(1e12))
    with in_db.begin(write=True) as in_txt:
        for i, path in enumerate(paths):
            label_index = get_label_index(path)
            image = caffe.io.load_image(path)
            image = caffe.io.resize_image(image, (IMAGE_SIZE, IMAGE_SIZE,))
            # height, width, channels to channels, height, width
            image = numpy.rollaxis(image, 2).astype(float)
            datum = caffe.io.array_to_datum(image, label=label_index)
            in_txt.put('{:0>5d}'.format(i), datum.SerializeToString())
            print '{0:0>8d}:{1}'.format(i, path)
    in_db.close()

    print 'complete created: {0}'.format(db_path)


def make_lmdbs():
    train_paths = glob.glob(TRAIN_DIR + '/*/*.jpg')
    val_paths = glob.glob(VAL_DIR + '/*/*.jpg')

    make_lmdb(TRAIN_LMDB, train_paths)
    make_lmdb(VAL_LMDB, val_paths)

if __name__ == "__main__":
    reset_dirs()
    split_train_val()
    make_lmdbs()
    write_labels_csv_file()
