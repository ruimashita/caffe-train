

```
$ docker-compose run train ./create_leveldb.sh
$ docker-compose run train ./create_mean.sh
$ docker-compose run train caffe train -solver solver.prototxt
```
