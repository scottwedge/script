#!/bin/bash

mysql -uroot -h 10.106.4.199 -p$MYPASSWORD -D Lab_Dev <<EOF
SET foreign_key_checks=0;
delete from server where id > 2;
truncate table association;
truncate table monitor_log;
truncate table monitor;
truncate table collector;
truncate table assertion;
truncate table handler;
truncate table action_log;
truncate table action;
truncate table scheduler;
truncate table event_log;
SET foreign_key_checks=1;
EOF