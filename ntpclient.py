#!/usr/bin/env python

'''
CS352 Assignment 1: Network Time Protocol
You can work with 1 other CS352 student
Sean Maye
DO NOT CHANGE ANY OF THE FUNCTION SIGNATURES BELOW
'''

from socket import socket, AF_INET, SOCK_DGRAM
import struct
from datetime import datetime
TIME1970 = 2208988800

def getNTPTimeValue(server="time.apple.com", port=123) -> (bytes, float, float):
    # add your code here 
    client=socket(AF_INET, SOCK_DGRAM)
    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    T1 = secs + float(time_difference.microseconds / 1000000.0)
    #data = struct.pack("!B", 0x1) + b'\x00' * 47
    data = b'\x1b' + b'\x00' * 47
    
    #client.connect(address)
    client.sendto(data,(server, port))
    data, _ = client.recvfrom(1024)
    #data is the packet
    client.close()
    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    T4= secs + float(time_difference.microseconds / 1000000.0)
    return (data, T1, T4)


def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    # add your code here 
    
    t2_seconds, t2_fraction = struct.unpack("!2I", pkt[32:40])
    t3_seconds, t3_fraction = struct.unpack("!2I", pkt[40:48])
    T2 = t2_seconds + (t2_fraction / 2**32)
    T3 = t3_seconds + (t3_fraction / 2**32)
    rtt=(T4-T1)- (T3-T2)
    offset = ((T2-T1)+(T3-T4))/2

    return (rtt, offset)

def getCurrentTime(server="time.apple.com", port=123, iters=20) -> float:
   data,T1,T4=getNTPTimeValue()
   t=struct.unpack("!12I",data)[10]
   currentTime=  t - TIME1970
   return currentTime


if __name__ == "__main__":

    print(getCurrentTime())
