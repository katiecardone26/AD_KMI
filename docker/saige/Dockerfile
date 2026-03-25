FROM ubuntu:20.04

WORKDIR /app

# set env variables
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENV R_VERSION=4.2.3 \
    DEBIAN_FRONTEND=noninteractive \
    PKG_CONFIG_PATH=/usr/lib/pkgconfig:/usr/share/pkgconfig

# install dependencies
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    ca-certificates \
    build-essential \
    gfortran \
    libreadline-dev \
    xorg-dev \
    libbz2-dev \
    liblzma-dev \
    curl \
    libxml2-dev \
    libcairo2-dev \
    libsqlite3-dev \
    libmariadbd-dev \
    libpq-dev \
    libssh2-1-dev \
    unixodbc-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libsodium-dev \
    libtool \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libboost-all-dev \
    pkg-config \
    wget \
    build-essential \
    cmake \
    libopenblas-base \
    python3-pip \
    liblapack-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Download and install R
    && wget -c https://cran.r-project.org/src/base/R-4/R-${R_VERSION}.tar.gz \
    && tar -xf R-${R_VERSION}.tar.gz \
    && cd R-${R_VERSION} \
    && ./configure \
    && make -j$(nproc) \
    && make install \
    && cd .. \
    && rm -rf R-${R_VERSION} R-${R_VERSION}.tar.gz \
    # install cget
    && pip3 install cget \
    # clone github
    && git clone https://github.com/saigegit/SAIGE.git \
    # install R packages
    && R -e "install.packages(c('rcmdcheck', 'urlchecker','miniUI','rversions'), repos='https://cloud.r-project.org/')"
RUN Rscript SAIGE/extdata/install_packages.R \
    && R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/BH/BH_1.78.0-0.tar.gz', repos=NULL, type='source')" \
    # install SAIGE
    && R CMD INSTALL SAIGE/ \
    # move SAIGE scripts to path
    && mv SAIGE/extdata/step1_fitNULLGLMM.R SAIGE/extdata/step2_SPAtests.R SAIGE/extdata/step3_LDmat.R SAIGE/extdata/createSparseGRM.R /usr/local/bin/ \
    # make scripts executable
    && chmod -R a+x /usr/local/bin/ \
    # remove SAIGE directory
    && rm -R SAIGE
# Force step_2 to use 1 single thread. More threads are ineffective
ENV OMP_NUM_THREADS=1

# Set environment variables for LAPACK
ENV LD_LIBRARY_PATH="/usr/lib:${LD_LIBRARY_PATH}"
ENV PKG_CONFIG_PATH="/usr/lib/pkgconfig:/usr/share/pkgconfig:${PKG_CONFIG_PATH}"

USER root
