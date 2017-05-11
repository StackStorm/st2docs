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

# Ugly stuff to get old st2 versions to pass 'make requirements' steps
sed -i 's/^ipython$/ipython<6.0.0/' st2/test-requirements.txt
sed -i 's/six==1\.9\.0/six==1.10.0/' st2/fixed-requirements.txt
sed -i 's/six==1\.9\.0/six==1.10.0/' st2/requirements.txt
sed -i 's/pip>=7\.1\.2,<8\.0\.0/pip>=8.1.2,<8.2/' st2/Makefile
sed -i 's/virtualenv>=13\.1\.2,<14\.0/virtualenv>=15.0.3,<15.1/' st2/fixed-requirements.txt
sed -i 's/req\.project_name/name/' st2/scripts/fixate-requirements.py
