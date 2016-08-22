#!/bin/sh

pushd `dirname $0` > /dev/null
ST2DOCSROOT="${PWD%/*}"
popd > /dev/null

docker build -t st2/st2docs -f $ST2DOCSROOT/Dockerfile $ST2DOCSROOT