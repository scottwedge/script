#!/bin/bash
deactivate
a=${1-1}
file=
case $a in
    1)
        file=Current_Build;;
    2)
        file=FortiExtender;;
    3)
        file=labMonitor;;
    *)
        echo 'error'
esac

cd /home/yangzhengchu/fortinet/$file
source venv/bin/activate
