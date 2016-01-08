# Caffe Net

```
$ docker-compose run train ./create_leveldb.sh
$ docker-compose run train ./create_mean.sh
```

```
$ docker-compose run train caffe train -solver solver.prototxt
```

```
$ docker-compose run train caffe train -solver solver.prototxt --weights /opt/caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel
```


# VGG

```
$ docker-compose run train ./create_lmdb.sh
$ docker-compose run train ./create_mean.sh
```

```
$ docker-compose run train caffe train -solver vgg.solver.prototxt
```

```
$ docker-compose run train caffe train -solver vgg.solver.prototxt --weights /opt/caffe/models/211839e770f7b538e2d8/VGG_ILSVRC_16_layers.caffemodel
```
