FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
  dumb-init \
  && rm -rf /var/lib/apt/lists/*

COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt 

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/entrypoint.sh"]
