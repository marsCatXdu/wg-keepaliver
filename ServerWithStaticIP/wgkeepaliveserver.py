import socket
import sys
import logging

class UDPListener(object):
    def __init__(self, port:int=23356, remote_ep={}):
        self.port = port
        self.remote_ep = remote_ep

    def listenUDP(self) -> tuple:
        local_endpoint = ('10.4.1.1', self.port)
        try:
            server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            server.bind(local_endpoint)
            data = server.recvfrom(1024)                        # udp 用 recvfrom，tcp 用 recv
            self.remote_ep = tuple([data[1][0], data[1][1]])
            server.sendto("received".encode(), self.remote_ep)
            return tuple([bytes.decode(data[0]), data[1]])      # data 是 bytes，可以 decode 成 str
        except IOError:
            print(IOError)


def main():
    logging.basicConfig(filename="wgkeepaliveserver_log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
    udp_listener = UDPListener()
    while True:
        try:
            logging.debug("listening udp")
            udp_listener.listenUDP()
            logging.debug("heard from client " + udp_listener.remote_ep[0] + ":" + str(udp_listener.remote_ep[1]))
            print("heard from client " + udp_listener.remote_ep[0] + ":" + str(udp_listener.remote_ep[1]))
            
        except KeyboardInterrupt as ki:
            print("\nCtrl+C pressed. Terminate.")
            sys.exit(1)

if __name__ == "__main__":
    main()
