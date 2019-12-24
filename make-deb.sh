#!/bin/bash

VERSION=$(cat VERSION)

set -x

dpkg-buildpackage

