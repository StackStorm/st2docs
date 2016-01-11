#!/bin/sh

ST2_DIRECTORY=st2

if [ -d $ST2_DIRECTORY ]; then
    rm -rf $ST2_DIRECTORY
fi

docs_version=`cat version.txt`

case $docs_version in
    *dev*)
        REQUIRED_BRANCH="master"
        ;;
    *)
        REQUIRED_BRANCH="v$docs_version"
        ;;
esac

echo "Cloning branch $REQUIRED_BRANCH of st2"
git clone -b $REQUIRED_BRANCH --depth 1 https://github.com/StackStorm/st2.git st2
