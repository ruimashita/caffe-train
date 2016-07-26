FROM ruimashita/caffe-cpu-with-models:rc3

env PATH $PATH:/opt/caffe/build/tools

RUN pip install lmdb

RUN bash /opt/caffe/data/ilsvrc12/get_ilsvrc_aux.sh
