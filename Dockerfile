FROM ubuntu:trusty
MAINTAINER Evan Cordell <cordell.evan@gmail.com>

## Prepare
RUN apt-get clean all && apt-get update && apt-get upgrade -y

# Build Tools
RUN apt-get install -y build-essential zlib1g-dev libssl-dev libreadline6-dev libyaml-dev && \
    apt-get install -y make wget tar git && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Install libsodium
RUN wget https://github.com/jedisct1/libsodium/releases/download/1.0.0/libsodium-1.0.0.tar.gz && \
  tar xzvf libsodium-1.0.0.tar.gz && \
  cd libsodium-1.0.0 && \
  ./configure && \
  make && make check && sudo make install && \
  cd .. && rm -rf libsodium-1.0.0 && \
  sudo ldconfig

# Install Python
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev python3-software-properties && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Ruby
RUN cd /tmp && \
  wget -q http://cache.ruby-lang.org/pub/ruby/2.1/ruby-2.1.2.tar.gz && \
  tar xzf ruby-2.1.2.tar.gz && \
  cd ruby-2.1.2 && \
  ./configure --enable-shared --prefix=/usr && \
  make && \
  make install && \
  cd .. && \
  rm -rf ruby-2.1.2* && \
  cd ..

# Install Node
ENV NODE_VERSION 0.11.14
ENV NPM_VERSION 2.1.6

RUN wget -q "http://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
  && tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
  && rm "node-v$NODE_VERSION-linux-x64.tar.gz" \
  && npm install -g npm@"$NPM_VERSION" \
  && npm cache clear

RUN apt-get update && \
    apt-get install -y python python-dev python-software-properties && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py --no-check-certificate -O - | python && \
    wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py --no-check-certificate -O - | python

# Install libmacaroons
RUN wget -O - http://ubuntu.hyperdex.org/hyperdex.gpg.key | apt-key add - && \
    echo "deb [arch=amd64] http://ubuntu.hyperdex.org trusty main" >> /etc/apt/sources.list.d/hyperdex.list && \
    apt-get update && \
    apt-get install -y python-macaroons && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install pymacaroons
RUN pip3 install pymacaroons

# Install ruby-macaroons
RUN gem install macaroons

# Install macaroons.js
RUN npm install -g macaroons.js
