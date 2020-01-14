FROM alpine:edge

# install ca-certificates so that HTTPS works consistently
RUN apk add --no-cache ca-certificates

RUN apk add --no-cache --update \
      aria2 \
      build-base \
      bash \
      python3 \
      python3-dev \
      py3-pip \
      libffi-dev \
      openssl-dev

RUN mkdir /bot
RUN chmod 777 /bot
WORKDIR /bot

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x aria.sh

CMD ["bash","start.sh"]
