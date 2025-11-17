FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    git \
    tree \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

RUN python -m pip install --upgrade pip

ARG PYTHON_ENV=teste_A3_docs_env
ENV PYTHON_ENV=$PYTHON_ENV

RUN mkdir /requirements

COPY requirements.txt set_python_env.sh /requirements/

RUN chmod +x /requirements/set_python_env.sh

RUN bash /requirements/set_python_env.sh $PYTHON_ENV

CMD ["bash"]
