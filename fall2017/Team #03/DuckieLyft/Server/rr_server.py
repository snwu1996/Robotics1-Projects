#! /usr/bin/env python
from Dobot import Dobot
import RobotRaconteur as RR


RRN = RR.RobotRaconteurNode.s


def main():
    port = 10001
    t1 = RR.LocalTransport()
    t1.StartServerAsNodeName("dobotRR")
    RRN.RegisterTransport(t1)

    t2 = RR.TcpTransport()
    t2.EnableNodeAnnounce()
    t2.StartServer(port)
    RRN.RegisterTransport(t2)
    
    my_dobot = Dobot('COM9')

    with open('dobotRR.robodef', 'r') as f:
        service_def = f.read()
    
    RRN.RegisterServiceType(service_def)
    RRN.RegisterService("dobotController", "dobotRR.Dobot", my_dobot)
    print "Connect string: tcp://localhost:" + str(port) + "/dobotRR/dobotController"
    my_dobot.loop()

    RRN.Shutdown()


if __name__ == '__main__':
    main()

