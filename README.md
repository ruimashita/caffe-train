# Caffe Net

```
$ docker-compose run docker ./create_leveldb.sh
$ docker-compose run docker ./create_mean.sh
```

```
$ docker-compose run docker caffe train -solver caffe_net/solver.prototxt
```

```
$ docker-compose run docker caffe train -solver caffe_net/solver.prototxt --weights /opt/caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel
```


# VGG

```
$ docker-compose run docker ./create_lmdb.sh
$ docker-compose run docker ./create_mean.sh
```

```
$ docker-compose run docker caffe train -solver vgg.solver.prototxt
```

```
$ docker-compose run docker caffe train -solver vgg.solver.prototxt --weights /opt/caffe/models/211839e770f7b538e2d8/VGG_ILSVRC_16_layers.caffemodel
```
