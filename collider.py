import sys
import socket
import time
import getopt

class Receiver():
    def __init__(self,listenport=50000,debug=False,timeout=5):
        self.timeout = timeout
        self.last_print = time.time()
        self.port = listenport
        self.host = ''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.settimeout(0.5)
        self.s.bind((self.host,self.port))
        self.messages = []

    def start(self):
        while True:
            try:
                try:
                    message, address = self.s.recvfrom(4096)
                    self.messages.append(message)
                except socket.timeout:
                    pass
                
                now = time.time()
                diff = now - self.last_print
                num_msg = len(self.messages)
                if num_msg > 0 and diff > self.timeout:
                    if num_msg > 1:
                        print "COLLISION!"
                    else:
                        print "%s" % self.messages[0]
                    self.messages = []
                    self.last_print = now 

            except (KeyboardInterrupt, SystemExit):
                exit()

if __name__ == "__main__":
    def usage():
        print "Usage: python collider.py [-p PORT] [-t TIMEOUT]"
        print ""
        print "EE122 collision example"
        print "-p PORT | --port=PORT The listen port, defaults to 33122"
        print "-t TIMEOUT | --timeout=TIMEOUT Collision check interval in seconds"
        print "-h | --help Print this usage message"
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                               "p:t:", ["port=", "timeout="])
    except:
        usage()
        exit()

    port = 33122
    debug = False
    timeout = 10

    for o,a in opts:
        if o in ("-p", "--port="):
            port = int(a)
        elif o in ("-t", "--timeout="):
            timeout = int(a)
        elif o in ("-d", "--debug="):
            debug = True
        else:
            print usage()
            exit()
    r = Receiver(port, debug, timeout)
    r.start()
