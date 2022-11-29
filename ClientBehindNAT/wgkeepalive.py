import socket
import time
import subprocess as sup
import logging
import sys

# Try to connect remote server (with a static ip address) via WireGuard
def try_connect_via_wg():
    remote_ep = ('10.4.1.1', 23356)     # local endpoint, using wg
    bytes_to_send = str.encode("{'data':'hello'}")
    UDP_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    logging.debug("Sent hello packet to " + remote_ep[0] + ":" + str(remote_ep[1]))
    for x in range(3):
        UDP_client_socket.settimeout(3)
        UDP_client_socket.sendto(bytes_to_send, remote_ep)
        buffer_size = 1024              # optimize for most of MTU
        logging.debug("the " + str(x) + " time trying to sayhello, waitting for response")
        try:
            msg_from_server = UDP_client_socket.recvfrom(buffer_size)
            logging.debug("response received, content: " + str(msg_from_server))
            return True
        except:
            continue
    return False

def restart_wg():
    down_command = "wg-quick down wg0"
    shutdown_current_wg = sup.Popen(down_command, shell=True, encoding='utf-8')
    shutdown_current_wg.wait()
    logging.debug("downing wg")
    up_command = "wg-quick up wg0"
    up_wg = sup.Popen(up_command, shell=True, encoding='utf-8')
    up_wg.wait()
    logging.debug("wg restarted")

def main():
    logging.basicConfig(filename="wgkeepalive_log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    while(True):
        hello_result = try_connect_via_wg()
        if hello_result:
            time.sleep(45)
        else:
            restart_wg()

if __name__ == "__main__":
    main()