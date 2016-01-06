#!/bin/sh

ST2_DIRECTORY=st2

if [ -d $ST2_DIRECTORY ]; then
    rm -rf $ST2_DIRECTORY
fi

REQUIRED_BRANCH=`git rev-parse --abbrev-ref HEAD`
git clone -b $REQUIRED_BRANCH --depth 1 https://github.com/StackStorm/st2.git st2
