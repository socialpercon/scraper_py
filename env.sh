#!/usr/bin/env bash
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/`basename "${BASH_SOURCE[0]}"`
BASE_DIR=`dirname $ABSOLUTE_PATH`
export PACKAGE_HOME=${BASE_DIR}
