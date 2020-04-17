#/bin/bash

if [ -z "$1" ]
then
    python3 anomaly.py 1
    python3 anomaly.py 2
    python3 anomaly.py 4 19
    python3 anomaly.py 5 54 
	python3 anomaly.py 6 17
	python3 anomaly.py 7 3 
	python3 anomaly.py 7 14 
	python3 anomaly.py 7 16 
	python3 anomaly.py 8 0 
	python3 anomaly.py 8 7 
	python3 anomaly.py 10 1 
	python3 anomaly.py 11 1 1
	#python3 anomaly.py 12 15

else
    python3 anomaly.py 4 20 
    python3 anomaly.py 5 50 
	python3 anomaly.py 6 15
	python3 anomaly.py 7 7 
	python3 anomaly.py 7 15 
	python3 anomaly.py 8 4 
	python3 anomaly.py 8 8 
	python3 anomaly.py 10 0 
	python3 anomaly.py 11 1 0
	python3 anomaly.py 11 1 0
	#python3 anomaly.py 12 14

fi

