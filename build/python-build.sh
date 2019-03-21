#!/usr/bin/env bash
mkdir -p /tmp/python
cd /tmp/python || exit 125
wget -qO- "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz" | tar -xJf -
mv ./* build
cd /build || exit 125
./configure --prefix=/usr \
  --with-ensurepip=install \
  --enable-shared \
  --with-system-expat \
  --with-system-ffi \
  --with-ensurepip=yes &&
  make &&
  make install
