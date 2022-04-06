#MAINTAINER Achraf Hmimou (ahmimou@cieautomotive.com)

FROM testing:node-red-build
USER root


RUN apt-get install -y python3-dev python3-pip python3-setuptools python3-wheel
RUN apt-get install -y python3-numpy python3-pandas 

# Install base utilities
# RUN apt-get update && \
#     apt-get install -y build-essentials  && \
#     apt-get install -y wget && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Install miniconda
# ENV CONDA_DIR /opt/conda
# RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#      /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
# ENV PATH=$CONDA_DIR/bin:$PATH


# RUN conda install -c intel scikit-learn
# RUN conda install -c intel tensorflow

USER node-red
RUN npm install node-red-contrib-machine-learning node-red-contrib-influxdb node-red-contrib-mssql-plus node-red-contrib-s7 node-red-contrib-python-function





