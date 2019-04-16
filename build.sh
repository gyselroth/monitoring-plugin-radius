#!/bin/sh

BASE_DIR=$(pwd)
BUILD_DEPS_DIR="$BASE_DIR/build_dependencies"
PYRAD_BUILD_DIR="$BUILD_DEPS_DIR/pyrad"
SCRIPT_DIR="$BASE_DIR/script"
DEPS_DIR="$SCRIPT_DIR/dependencies"

if [ -d $PYRAD_BUILD_DIR ]
then
    cd $PYRAD_BUILD_DIR
    # update pyrad
    echo "# update pyrad"
    git pull origin master
else
    # clone pyrad
    mkdir $BUILD_DEPS_DIR
    cd $BUILD_DEPS_DIR
    echo "# clone pyrad"
    git clone https://github.com/wichert/pyrad
    cd $PYRAD_BUILD_DIR
fi

# download pyrad dependencies into check_radius directory
echo "# download pyrad dependencies into check_radius directory"
pip download -r requirements.txt -d $BUILD_DEPS_DIR
cd $BUILD_DEPS_DIR
mkdir -p $DEPS_DIR
for dependency in $(cat $PYRAD_BUILD_DIR/requirements.txt)
do
  unzip -u $dependency*.whl
  if [ -d $dependency ]
  then
    cp -r $dependency $DEPS_DIR/$dependency
  fi
  if [ -f $dependency.py ]
  then
    cp $dependency.py $DEPS_DIR/
  fi
done
cd $PYRAD_BUILD_DIR

# build pyrad to check_radius directory
echo "# build pyrad into check_radius directory"
python setup.py build --build-purelib  $DEPS_DIR/
cp $PYRAD_BUILD_DIR/example/dictionary $DEPS_DIR/
touch $DEPS_DIR/__init__.py

cd $SCRIPT_DIR
# zip check_radius directory
echo "# zip check_radius directory"
tmp=$(mktemp -u --suffix=.zip /tmp/$0.XXXXXX)
zip -r $tmp *

cd $BASE_DIR
# generate executable
echo "# generate executable"
echo '#!/usr/bin/env python' | cat - $tmp > check_radius
chmod +x check_radius
ls check_radius

# cleanup
echo "# cleanup"
rm $tmp
