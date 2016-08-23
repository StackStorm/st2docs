#!/bin/sh

pushd `dirname $0` > /dev/null
ST2DOCSROOT="${PWD%/*}"
popd > /dev/null

docker run --rm -it -p 127.0.0.1:8000:8000 \
  -v "$ST2DOCSROOT"/docs/source:/st2docs/docs/source st2/st2docs