# Setup

`/data_set/images/{label}/**.jpg` となるように、画像を配置する。


# Caffe Net

```
$ docker-compose run docker python create_lmdb.py
$ docker-compose run docker ./create_mean.sh
```

```
$ docker-compose run docker caffe train -solver caffe_net/solver.prototxt > caffe.log
```

```
$ docker-compose run docker caffe train -solver caffe_net/solver.prototxt --weights /opt/caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel > caffe.log
```


# VGG

```
$ docker-compose run docker python create_lmdb.py
$ docker-compose run docker ./create_mean.sh
```

```
$ docker-compose run docker caffe train -solver vgg.solver.prototxt > caffe.log
```

```
$ docker-compose run docker caffe train -solver vgg.solver.prototxt --weights /opt/caffe/models/211839e770f7b538e2d8/VGG_ILSVRC_16_layers.caffemodel > caffe.log
```

# plot 

```
$ mkdir plot
$ docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 0 plot/0.png caffe.log && \
docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 1 plot/1.png caffe.log && \
docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 2 plot/2.png caffe.log  && \
docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 3 plot/3.png caffe.log  && \
docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 4 plot/4.png caffe.log  && \
docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 5 plot/5.png caffe.log  && \
docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 6 plot/6.png caffe.log  && \
docker-compose run docker python /opt/caffe/tools/extra/plot_training_log.py.example 7 plot/7.png caffe.log
```
