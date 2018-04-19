FROM dockerhub.datacamp.com:443/python-base-prod:20

ARG GH_TOKEN

RUN mkdir -p /usr/local/pkg
WORKDIR /usr/local/pkg

COPY . pythonwhat/
RUN pip3 install -r pythonwhat/requirements.txt
RUN pip3 install protobackend
RUN git clone https://$GH_TOKEN@github.com/datacamp/pythonbackend.git && pip3 install --no-dependencies ./pythonbackend && rm -rf pythonbackend

WORKDIR /usr/local/pkg/pythonwhat
RUN rm -rf tests/__pycache__
