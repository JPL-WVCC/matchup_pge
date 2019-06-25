FROM hysds/pge-base

MAINTAINER leipan "leipan@jpl.nasa.gov"
LABEL description="wvcc CrIS VIIRS matchup PGE container"

USER root
RUN set -ex \
 && conda install numpy \
 && conda install netCDF4 \
 && conda install pykdtree \
 && conda install h5py 

USER ops
COPY . /home/ops/matchup_pge
### COPY /tmp/data /tmp/
RUN set -ex \
 && cd /tmp \
 && git clone git@github.com:leipan/CrIS_VIIRS_collocation-master.git \
 && mv CrIS_VIIRS_collocation-master /home/ops

# set entrypoint
WORKDIR /home/ops
CMD ["/bin/bash", "--login"]


