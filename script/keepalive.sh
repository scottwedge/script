#!/bin/bash
while true
do
	if ! ps -ef | grep "python manage.py runserver"| grep -v grep &>/dev/null 
	then
		date 
		echo "manage down" 
		source /home/zcyang/fortinet/Current_Build/venv/bin/activate && cd /home/zcyang/fortinet/Current_Build/AutomationUI_Dev && sh start_orig.sh
	    continue	
	fi

	if ! ps -ef | grep "python.*celery" | grep -v grep &>/dev/null
	then
		date 
		echo "celery down" 
		source /home/zcyang/fortinet/Current_Build/venv/bin/activate && cd /home/zcyang/fortinet/Current_Build/AutomationUI_Dev && sh start_orig.sh
	    continue	
	fi

	if ! ps -ef | grep "python.*schedule_rpc_service_temp" | grep -v grep &>/dev/null
	then
		date 
		echo "rpc down" 
		source /home/zcyang/fortinet/Current_Build/venv/bin/activate && cd /home/zcyang/fortinet/Current_Build/AutomationUI_Dev && sh start_orig.sh
	    continue	
	fi
    sleep 100 
done