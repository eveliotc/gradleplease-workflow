#!/bin/sh
AWFILENAME='GradlePlease.alfredworkflow'
rm $AWFILENAME
zip -r $AWFILENAME . -x ".*" "*.pyc" "*.alfredworkflow" "demo.gif" "package.sh"