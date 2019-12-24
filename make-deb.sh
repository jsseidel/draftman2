#!/bin/bash

VERSION=$(cat VERSION)

make dist-build
rm -rf ./install_files
mkdir -p ./install_files/opt/draftman2
mkdir -p ./install_files/usr/share/applications
cp -r dist/lib/Draftman2-${VERSION}/* ./install_files/opt/draftman2/.
cp draftman2.desktop ./install_files/usr/share/applications/.
dpkg-buildpackage

