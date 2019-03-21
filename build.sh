#!/usr/bin/env bash
DOCKER_TAG="zstlib-rpm-builder"

mkdir -p rpms

echo -en "\nTesting image"
IMAGE_ID=$(docker images -f "reference=$DOCKER_TAG" -q)

if [[ -z "$IMAGE_ID" ]]; then
  echo -en "\n\nBuilding docker image..."
  docker build . -t ${DOCKER_TAG}
fi

echo -en "\nBuilding rpm packages:"
echo -en "\npython27..."
docker run -it --rm \
  -v "$PWD/rpms":/rpms \
  -v "$PWD":/build/src \
  --env-file build.env \
  --env PYTHON_VERSION="python27" \
  --env PYTHON_BIN="/usr/bin/python2.7" \
  --env PYTHON_PIP_BIN="/usr/bin/pip2.7" \
  --entrypoint /build/rpm-build.sh \
  "$DOCKER_TAG"

echo -en "\npython37..."
docker run -it --rm \
  -v "$PWD/rpms":/rpms \
  -v "$PWD":/build/src \
  --env-file build.env \
  --env PYTHON_VERSION="python37" \
  --env PYTHON_BIN="/usr/bin/python3.7" \
  --env PYTHON_PIP_BIN="/usr/bin/pip3.7" \
  --entrypoint /build/rpm-build.sh \
  "$DOCKER_TAG"
