#!/bin/sh

REPO_DIR=orquesta

if [ -d $REPO_DIR ]; then
    rm -rf $REPO_DIR
fi

# Only supports master branch for duration of beta.
REQUIRED_BRANCH="master"

echo "Cloning branch $REQUIRED_BRANCH of orquesta..."
git clone -b $REQUIRED_BRANCH https://github.com/StackStorm/orquesta.git ${REPO_DIR}

echo "Copying files to local st2docs repo..."
cp ${REPO_DIR}/docs/source/overview.rst ./docs/source/orquesta/overview.rst
cp ${REPO_DIR}/docs/source/context.rst ./docs/source/orquesta/context.rst
cp ${REPO_DIR}/docs/source/expressions.rst ./docs/source/orquesta/expressions.rst
cp ${REPO_DIR}/docs/source/yaql.rst ./docs/source/orquesta/yaql.rst
cp ${REPO_DIR}/docs/source/jinja.rst ./docs/source/orquesta/jinja.rst
cp -R ${REPO_DIR}/docs/source/languages ./docs/source/orquesta
cp -R ${REPO_DIR}/docs/source/development ./docs/source/orquesta
