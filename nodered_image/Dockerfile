#MAINTAINER Achraf Hmimou (ahmimou@cieautomotive.com)


# La base sera node-red
# FROM nodered/node-red
# USER root
# RUN apk add python3-dev
# RUN apk add py3-pip

# RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev
# RUN apk add py3-pip py3-numpy 
# # py3-pandas py3-scikit-learn
# # RUN pip install tensorflow
# USER node-red

# RUN npm install node-red-contrib-machine-learning node-red-contrib-influxdb node-red-contrib-mssql-plus node-red-contrib-s7


# RUN pip3 install tensorflow 


# docker run -it -p 1880:1880 -v myNodeREDdata:/data --name mynodered nodered/node-red

FROM testing:node-red-build
USER root
# RUN apt-get install -y python3-dev python3-pip python3-setuptools python3-wheel


RUN apt-get install -y python3-dev python3-pip python3-setuptools python3-wheel
RUN apt-get install -y python3-numpy python3-pandas 
RUN pip3 install pandas 
RUN pip3 install 'influxdb-client[ciso]'

# Install base utilities
# RUN apt-get update && \
#     apt-get install -y build-essentials  && \
#     apt-get install -y wget && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH


RUN conda install -c intel scikit-learn
RUN conda install -c intel tensorflow

USER node-red
RUN npm install node-red-contrib-machine-learning node-red-contrib-influxdb node-red-contrib-mssql-plus node-red-contrib-s7 node-red-contrib-python-function node-red-contrib-uibuilder





