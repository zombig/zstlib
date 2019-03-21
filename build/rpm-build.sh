#!/usr/bin/env bash

cat <<EOF
Running env:
  PYTHON_VERSION:     $PYTHON_VERSION
  PYTHON_BIN:         $PYTHON_BIN
  PYTHON_PIP_BIN:     $PYTHON_PIP_BIN
  ---
  LICENSE:            $LICENSE
  ---
  RPMS_DIR:           $RPMS_DIR
  LOG_LEVEL:          $LOG_LEVEL
  WITH_DEPENDENCIES:  ${WITH_DEPENDENCIES:-False}
  ---
  PWD:                $PWD
  ---
  Current working dir:
    $(tree -L 3)
  ---
EOF

fpm -f --python-package-name-prefix $PYTHON_VERSION \
  --package $RPMS_DIR \
  --license $LICENSE \
  --python-bin $PYTHON_BIN \
  --python-pip $PYTHON_PIP_BIN \
  --log $LOG_LEVEL \
  -s python -t rpm /build/src/setup.py

cd /build/src || exit 125
$PYTHON_BIN setup.py sdist bdist_wheel
