#!/bin/sh

DCF_DIRECTORY=dcfabric

if [ -d $DCF_DIRECTORY ]; then
    rm -rf $DCF_DIRECTORY
fi

# For now we'll always pull from master
# TODO: Figure out how to have Network Essentials branch versions
#docs_version=`cat version.txt | cut -d '.' -f 1,2`


#case $docs_version in
#    *dev*)
#        REQUIRED_BRANCH="master"
#        ;;
#    *)
#        REQUIRED_BRANCH="v$docs_version"
#        ;;
#esac

#if [ ! -z $BWC_BRANCH ]; then
#    REQUIRED_BRANCH=$BWC_BRANCH
#fi

REQUIRED_BRANCH="master"

echo "Cloning branch $REQUIRED_BRANCH of DC Fabric Suite"
git clone -b $REQUIRED_BRANCH --depth 1 https://github.com/StackStorm/sandbox-actions $DCF_DIRECTORY
