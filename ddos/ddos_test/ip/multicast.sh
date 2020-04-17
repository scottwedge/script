if [ -z "$1" ]
then
    ping 224.0.0.1 -c 1 -W 1 | grep loss
    ping 239.255.255.254 -c 1 -W 1 | grep loss
    y_hping3 -2 -a 224.0.0.1 -c 1
    y_hping3 -2 -a 239.255.255.254 -c 1
else
    ping 240.0.0.1 -c 1 -W 1 | grep loss
    ping 223.255.255.254 -c 1 -W 1 | grep loss
    y_hping3 -2 -a 240.0.0.1 -c 1
    y_hping3 -2 -a 223.255.255.254 -c 1
fi
