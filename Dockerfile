FROM ruimashita/caffe-gpu-with-models:rc3

RUN pip install lmdb

RUN bash /opt/caffe/data/ilsvrc12/get_ilsvrc_aux.sh
