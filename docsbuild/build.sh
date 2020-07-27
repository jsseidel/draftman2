#!/bin/bash

ACTIVITY=$1
OUT_DIR=$2

if [[ "$ACTIVITY" == "post" ]] ; then
    echo "Copying ./$OUT_DIR/* to ../docs/."
    cp -vr ./$OUT_DIR/* ../docs/.
fi
