FROM wzhou88/saige:1.3.6
WORKDIR /app

USER root

USER root
COPY snpinfo_mult_1kg_hm3_map_b37_b38 /app/snpinfo_mult_1kg_hm3_map_b37_b38
COPY snpinfo_mult_ukbb_hm3_map_b37_b38 /app/snpinfo_mult_ukbb_hm3_map_b37_b38

RUN chmod +r /app/snpinfo_mult_1kg_hm3_map_b37_b38
RUN chmod +r /app/snpinfo_mult_ukbb_hm3_map_b37_b38

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash libtiff5-dev libz-dev g++ gcc git wget tar unzip make \
    && rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

ENV PATH=$CONDA_DIR/bin:$PATH

RUN mkdir plink

RUN wget -P plink https://s3.amazonaws.com/plink2-assets/alpha5/plink2_linux_x86_64_20240526.zip

RUN wget -P plink https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20231211.zip

WORKDIR plink

RUN unzip plink2_linux_x86_64_20240526.zip

RUN unzip plink_linux_x86_64_20231211.zip

RUN rm -rf plink2_linux_x86_64_20240526.zip

RUN rm -rf plink_linux_x86_64_20231211.zip

RUN mv plink2 /usr/bin

RUN mv plink /usr/bin

WORKDIR /app

RUN git clone --depth 1 -b master https://github.com/getian107/PRScsx.git

RUN wget https://www.geenivaramu.ee/tools/GWAMA_v2.2.2.zip

RUN unzip GWAMA_v2.2.2.zip

RUN make

RUN git clone https://github.com/PMBB-Informatics-and-Genomics/NEAT-Plots.git

RUN mv NEAT-Plots/manhattan-plot/ /app/

ARG BIOFILTER_VERSION=2.4.3

RUN wget https://github.com/RitchieLab/biofilter/releases/download/Biofilter-${BIOFILTER_VERSION}/biofilter-${BIOFILTER_VERSION}.tar.gz -O biofilter.tar.gz

RUN tar -zxvf biofilter.tar.gz --strip-components=1 -C /app/

USER $CONDA_USER


RUN conda install -y -n base -c conda-forge -c bioconda scipy=1.11.4 h5py libtiff bgenix dominate wget conda-build scipy pandas seaborn matplotlib numpy apsw sqlite && \
    conda clean --all --yes

WORKDIR /app/manhattan-plot/

RUN conda develop .

WORKDIR /app/

RUN /opt/conda/bin/python setup.py install

RUN chmod a+r /app/biofilter.py

RUN chmod a+x /app/biofilter.py

RUN ln -s /opt/conda/lib/libtiff.so.6 /opt/conda/lib/libtiff.so.5

USER root
