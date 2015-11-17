

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
