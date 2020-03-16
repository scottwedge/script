#!/bin/bash
directorys=`curl http://172.22.15.15:7273  | grep href | gawk -F \" '{print $2}' | grep \/`
directorys=". "${directorys}
echo ${directorys}
for d in $directorys
do
	if [ "${d}" = "." ]
	then
		d=""	
	fi
	echo "curl http://172.22.15.15:7273/${d}  | grep href | gawk -F \" '{print $2}' | grep -v \/"
	files=`curl http://172.22.15.15:7273/${d}  | grep href | gawk -F \" '{print $2}' | grep -v \/`
	mkdir dubo/$d
	for f in $files
	do
		cmd="curl http://172.22.15.15:7273/$d${f} --output dubo/$d$f"
		echo $cmd
		$cmd
	done
done
