#!/bin/sh

IPFABRIC_DIRECTORY=ipfabric

if [ -d $IPFABRIC_DIRECTORY ]; then
    rm -rf $IPFABRIC_DIRECTORY
fi

docs_version=`cat version.txt | cut -d '.' -f 1,2`

case $docs_version in
    *dev*)
        REQUIRED_BRANCH="master"
        ;;
    *)
        REQUIRED_BRANCH="v$docs_version"
        ;;
esac

if [ ! -z $BWC_BRANCH ]; then
    REQUIRED_BRANCH=$BWC_BRANCH
fi

echo "Cloning branch $REQUIRED_BRANCH of ipfabric docs"
git clone -b $REQUIRED_BRANCH --depth 1 https://github.com/extremenetworks/ipfabric-docs.git ipfabric
