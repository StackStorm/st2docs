#!/bin/sh

IPFABRIC_DIRECTORY=ipfabric

if [ -d $IPFABRIC_DIRECTORY ]; then
    rm -rf $IPFABRIC_DIRECTORY
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

echo "Cloning branch $REQUIRED_BRANCH of ipfabric docs"
git clone -b $REQUIRED_BRANCH --depth 1 https://github.com/StackStorm/ipfabric-docs.git ipfabric
