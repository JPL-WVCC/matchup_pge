FROM hysds/pge-base

MAINTAINER leipan "leipan@jpl.nasa.gov"
LABEL description="wvcc CrIS VIIRS matchup PGE container" \
      Version=1.0.0 \
      Vendor="JPL"

USER root
RUN source /opt/conda/bin/activate root \
 && conda config --add channels conda-forge \
 && conda install numpy \
 && conda install netCDF4 \
 && conda install pykdtree \
 && conda install h5py \
 && conda install basemap 

RUN yum -y update && yum -y --setopt=tsflags=nodocs install    \
      gcc-c++                                   \
      build-essential                           \
      make                                      \
      && yum clean all                          

USER ops
COPY . /home/ops/matchup_pge
RUN set -ex \
 && echo "export PATH=$PATH:/home/ops/local/dmtcp_installation/bin" >> /home/ops/.bashrc \
 && echo "alias h='history'"  >> /home/ops/.bashrc \
 && cd /tmp \
 && rm -rf CrIS_VIIRS_collocation-master \
 && git clone https://github.com/leipan/CrIS_VIIRS_collocation-master.git \
 && mv CrIS_VIIRS_collocation-master /home/ops/

RUN mkdir -p /home/ops/dmtcp
RUN mkdir -p /home/ops/local/dmtcp_installation
RUN mkdir -p /home/ops/navp

WORKDIR /home/ops/dmtcp
RUN git clone https://github.com/dmtcp/dmtcp.git /home/ops/dmtcp && \
      git checkout master &&                    \
      git log -n 1
RUN git clone https://leipan:e47e4b23ab852c2ba732260183b12033ad591018@github.com/leipan/navp.git /home/ops/navp

RUN ./configure --prefix=/home/ops/local/dmtcp_installation && make -j 2 && make install

# set entrypoint
WORKDIR /home/ops
CMD ["/bin/bash", "--login"]


