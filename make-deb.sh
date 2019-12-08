#!/bin/bash

mkdir -p ./install_files/opt/draftman2
mkdir -p ./install_files/usr/share/applications
cp -r dist/* ./install_files/opt/draftman2/.
cp draftman2.desktop ./install_files/usr/share/applications/.
dpkg-buildpackage

