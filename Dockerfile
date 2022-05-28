FROM ubuntu:20.04

WORKDIR /usr/src/app
SHELL ["/bin/bash", "-c"]
RUN chmod 777 /usr/src/app
RUN apt-get -qq update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y tzdata aria2 git python3 python3-pip \
    locales python3-lxml \
    curl pv jq ffmpeg \
    p7zip-full p7zip-rar \
    libcrypto++-dev libssl-dev \
    libc-ares-dev libcurl4-openssl-dev \
    libsqlite3-dev libsodium-dev && \
    curl -L https://github.com/lzzy12/megasdkrest/releases/download/v0.1.14-rebuild/megasdkrest-$(cpu=$(uname -m); if [[ "$cpu" == "x86_64" ]]; then    echo "amd64"; elif [[ "$cpu" == "x86" ]]; then    echo "i386"; elif [[ "$cpu" == "aarch64" ]]; then    echo "arm64"; else    echo $cpu; fi) -o /usr/local/bin/megasdkrest && \
    chmod +x /usr/local/bin/megasdkrest

COPY requirements.txt .
COPY extract /usr/local/bin
RUN chmod +x /usr/local/bin/extract
RUN pip3 install --no-cache-dir -r requirements.txt && \
    apt-get -qq purge git

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY . .
COPY netrc /root/.netrc
RUN chmod +x aria.sh

CMD ["bash","start.sh"]
