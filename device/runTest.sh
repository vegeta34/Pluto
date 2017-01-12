#!/bin/bash
cd ${0%/*}
adb devices -l
adb shell ls

python ml_tester.py 1>upload.dir/stanrd.txt 2>upload.dir/out.txt
