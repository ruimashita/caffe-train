# -*- coding: utf-8 -*-
import csv
import os
import os.path
import glob
import random
import shutil

WORK_DIR = '/home/docker'

DATASET_DIR = WORK_DIR + '/data_set'
IMAGES_DIR = DATASET_DIR + '/images'
TRAIN_DIR = DATASET_DIR + '/train'
VAL_DIR = DATASET_DIR + '/val'
TRAIN_TXT = DATASET_DIR + '/train.txt'
VAL_TXT = DATASET_DIR + '/val.txt'

LABELS_CSV_FILE = WORK_DIR + '/data_set/labels.csv'

SPLIT_VAL_RATE = 2  #


def reset_dir(dir_path):
    print "delete and make dir: {}".format(dir_path)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)


def reset_txt(path):
    if os.path.exists(path):
        os.remove(path)

    open(path, 'a').close()


def init():
    reset_dir(DATASET_DIR)

    reset_txt(TRAIN_TXT)
    reset_txt(VAL_TXT)

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
    paths = glob.glob(IMAGES_DIR + '/*/*.jpg')
    paths.sort()

    print 'exec split train val. all images num: {}'.format(len(paths))

    for path in paths:
        rand = random.randint(1, 10)
        label_name = get_label_name(path)
        basename = os.path.basename(path)

        if rand <= SPLIT_VAL_RATE:
            print 'split to val: {}'.format(path)
            dir_name = '{0}/{1}'.format(VAL_DIR, label_name)
            file_path = '{0}/{1}'.format(dir_name, basename)
            line = "{0} {1}".format(file_path, labels().index(label_name))
            write_file(VAL_TXT, line)
        else:
            print 'split to train: {}'.format(path)
            dir_name = '{0}/{1}'.format(TRAIN_DIR, label_name)
            file_path = '{0}/{1}'.format(dir_name, basename)
            line = "{0} {1}".format(file_path, labels().index(label_name))
            write_file(TRAIN_TXT, line)
        shutil.copy(path, dir_name)


def write_file(path, line):
    with open(path, 'a') as f:
        f.write(line + "\n")

if __name__ == "__main__":
    init()
    split_train_val()
    write_labels_csv_file()
