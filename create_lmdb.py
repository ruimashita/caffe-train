# -*- coding: utf-8 -*-
import csv
import os
import os.path
import sys
import glob
import random

import caffe
from caffe.proto import caffe_pb2
import h5py
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

def make_hd5(db_path, paths):
    print 'create db: {0}'.format(db_path)
    os.system('rm -rf ' + db_path)    
    random.shuffle(paths)

    paths = paths[:20]
    datas = numpy.zeros([len(paths), 3, 256, 256], numpy.float64)
    data_labels = numpy.zeros([len(paths), 2], numpy.float32)
    
    def get_image(path):
        image = caffe.io.load_image(path)
        image = caffe.io.resize_image(image, (IMAGE_SIZE, IMAGE_SIZE,))
        # height, width, channels to channels, height, width
        image = numpy.rollaxis(image, 2).astype(float)
        return image
    
    for i, path in enumerate(paths):
        label_index = get_label_index(path)
        image = get_image(path)
        print image.shape
        print image.dtype
        datas[i, : ,: ,:] = image
        data_labels[i, :] = [label_index, label_index]
        print '{0:0>8d}:{1}'.format(i, path)

    f = h5py.File(db_path, "w")
    f.create_dataset("data", data=datas,  compression="gzip", compression_opts=4)
    f.create_dataset("label", data=data_labels,  compression="gzip", compression_opts=4)
    f.close()
    print data_labels

def make_lmdbs():
    train_paths = glob.glob(TRAIN_DIR + '/*/*.jpg')
    val_paths = glob.glob(VAL_DIR + '/*/*.jpg')

    # make_hd5(TRAIN_LMDB, train_paths)
    # make_hd5(VAL_LMDB, val_paths)
    make_lmdb(TRAIN_LMDB, train_paths)
    make_lmdb(VAL_LMDB, val_paths)


def augmentation(paths):

    for path in paths:
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)
        img = PIL.Image.open(path)

        for i in range(-20, 20 + 1, 5):
            if i == 0:
                continue
            out = "{0}/{1}_{2}".format(dir_name, i, base_name)

            rgba_img = img.convert('RGBA')
            # rotated image
            rot_img = rgba_img.rotate(i, expand=1)
            # a white image same size as rotated image
            white_img = PIL.Image.new('RGBA', rot_img.size, (255,)*4)
            # create a composite image using the alpha layer of rot as a mask
            tmp = PIL.Image.composite(rot_img, white_img, rot_img)
            # save your work (converting back to mode='1' or whatever..)
            tmp.convert(img.mode).save(out)
            print "save rotate {0}: {1}".format(i, out)


def augmentations():
    train_paths = glob.glob(TRAIN_DIR + '/*/*.jpg')
    val_paths = glob.glob(VAL_DIR + '/*/*.jpg')
    augmentation(train_paths)
    augmentation(val_paths)

if __name__ == "__main__":
    reset_dirs()
    split_train_val()
    augmentations()
    make_lmdbs()
    write_labels_csv_file()
