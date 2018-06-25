#!/bin/sh

REPO_DIR=orchestra

if [ -d $REPO_DIR ]; then
    rm -rf $REPO_DIR
fi

# Only supports master branch for duration of beta.
REQUIRED_BRANCH="master"

echo "Cloning branch $REQUIRED_BRANCH of orchestra..."
git clone -b $REQUIRED_BRANCH https://github.com/StackStorm/orchestra.git ${REPO_DIR}

echo "Copying files to local st2docs repo..."
cp ${REPO_DIR}/docs/source/overview.rst ./docs/source/orchestra/overview.rst
cp ${REPO_DIR}/docs/source/context.rst ./docs/source/orchestra/context.rst
cp ${REPO_DIR}/docs/source/expressions.rst ./docs/source/orchestra/expressions.rst
cp ${REPO_DIR}/docs/source/yaql.rst ./docs/source/orchestra/yaql.rst
cp ${REPO_DIR}/docs/source/jinja.rst ./docs/source/orchestra/jinja.rst
cp -R ${REPO_DIR}/docs/source/languages ./docs/source/orchestra
