#!/usr/bin/env bash

CURRENT_DIR="$(cd "`dirname "$0"`"; pwd)"
export PYTHONPATH=${CURRENT_DIR}/../src/python:${CURRENT_DIR}:${PYTHONPATH}
NOSE_NOCAPUTRE=1

dir=.


if [ empty$1 = empty ]; then
    lim="tests"
else
    lim="tests.test_$1"
fi

if [ empty$coverage != empty ]; then
    args="--with-coverage"
else
    args=""
    echo "Call with coverage=1 to run coverage tests"
fi
(cd $dir && nosetests -vs $lim $args --cover-package=package_name)

