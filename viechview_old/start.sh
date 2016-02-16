#!/bin/sh
kill $(pgrep -f 'makeScreen')
kill $(pgrep -f 'serv.py')
python serv.py 31337 &
python -m SimpleHTTPServer 80 &
./makeScreen.sh 1
