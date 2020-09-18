FROM ubuntu:20.04
WORKDIR /usr/src/app
# http://bugs.python.org/issue19846
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN chmod 777 /usr/src/app
RUN apt-get -qq update && \
    apt-get -qq install -y tzdata aria2 git python3 python3-pip \
    locales python3-lxml \
    curl pv jq ffmpeg \
    p7zip-full p7zip-rar
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    apt-get -qq purge git
COPY . .
COPY netrc /root/.netrc
RUN chmod +x aria.sh
CMD ["bash","start.sh"]
