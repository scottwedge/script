#!/bin/bash

tables=`mysql -h 10.106.4.199 -uroot -p$MYPASSWORD -D Lab_Dev -Bse "show tables" 2> /dev/null`

l=
for table in $tables
do
    selectcommand="select count(*) from "${table}\;
    l=$l${selectcommand}
done
results=`mysql -h 10.106.4.199 -uroot -p$MYPASSWORD -D Lab_Dev -Bse "$l" 2> /dev/null`

num=`echo $tables | wc -w`

tables=( $tables )
results=( $results )

#for ((i=1;i<=$num;i++))
#do
#    echo -e $tables\\n$results | gawk  -v n=$i '{print $n}'
#done

for ((i=0;i<$num;i++))
do
    printf "%-25s%d\n" ${tables[$i]} ${results[$i]}
done