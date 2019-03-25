FROM centos:7

LABEL name="zstlib" \
  version="0.1.0"

ENV PYTHON_VERSION="3.7.1"
ENV LD_LIBRARY_PATH="/usr/lib:/usr/lib64"

# Install base/develop packages
RUN true \
  && yum install -y epel-release \
  && yum group install -y "Development Tools" \
  && yum install -y ruby-devel gem libffi-devel libsqlite3x-devel \
    sqlite-devel wget zlib-devel expat-devel python2-pip \
    openssl openssl-devel tree \
  && yum -y clean all \
  && echo "gem: --no-ri --no-rdoc --no-document" > ~/.gemrc \
  && gem install fpm \
  && gem cleanup all \
  && true

# Install python and dependencies
COPY build/python-build.sh /python-build.sh
RUN chmod +x /python-build.sh; /python-build.sh; \
    /bin/python -m pip install wheel; \
    /bin/python3 -m pip install wheel

# Prepare build directory
WORKDIR /build
COPY build/rpm-build.sh /build/rpm-build.sh
RUN chmod +x /build/rpm-build.sh
