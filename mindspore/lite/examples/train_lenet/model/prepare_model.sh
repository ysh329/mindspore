#!/bin/bash

echo "============Exporting=========="
if [ -n "$1" ]; then
  DOCKER_IMG=$1
  docker run -w $PWD --runtime=nvidia -v /home/$USER:/home/$USER --privileged=true ${DOCKER_IMG} /bin/bash -c "PYTHONPATH=../../../../../model_zoo/official/cv/lenet/src python lenet_export.py; chmod 444 lenet_tod.mindir; rm -rf __pycache__"
else
  echo "MindSpore docker was not provided, attempting to run locally"
  PYTHONPATH=../../../../../model_zoo/official/cv/lenet/src python lenet_export.py
fi


CONVERTER="../../../build/tools/converter/converter_lite"
if [ ! -f "$CONVERTER" ]; then
  if ! command -v converter_lite &> /dev/null
  then
    tar -xzf ../../../../../output/mindspore-lite-*-converter-linux-x64.tar.gz --strip-components 2 --wildcards --no-anchored converter_lite libmindspore_gvar.so
    tar -xzf ../../../../../output/mindspore-lite-*-converter-linux-x64.tar.gz --strip-components 4 --wildcards --no-anchored libglog.so.0
    if [ -f ./converter_lite ]; then
      CONVERTER=./converter_lite
    else
      echo "converter_lite could not be found in MindSpore build directory nor in system path"
      exit 1
    fi
  else
    CONVERTER=converter_lite
  fi
fi


echo "============Converting========="
LD_LIBRARY_PATH=./ $CONVERTER --fmk=MINDIR --trainModel=true --modelFile=lenet_tod.mindir --outputFile=lenet_tod

