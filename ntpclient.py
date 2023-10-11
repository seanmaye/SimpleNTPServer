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
    #make socket
    client=socket(AF_INET, SOCK_DGRAM)
    #get T1
    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    T1 = secs + float(time_difference.microseconds / 1000000.0)
    data = struct.pack("!B", 1)
    #data = b'\x1b' + b'\x00' * 47
   
    #send packet
    client.sendto(data,(server, port))
    data, _ = client.recvfrom(1024)
    client.close()
    #get T4
    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    T4= secs + float(time_difference.microseconds / 1000000.0)
    return (data, T1, T4)


def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    # add your code here 
    #extract t2 
    t2_seconds, t2_fraction = struct.unpack("!2I", pkt[32:40])
    #extract t3
    t3_seconds, t3_fraction = struct.unpack("!2I", pkt[40:48])
    #convert unix time
    t2_seconds-=TIME1970
    t3_seconds-=TIME1970
    #convert to float
    T2 = t2_seconds + (t2_fraction / 2**32)
    T3 = t3_seconds + (t3_fraction / 2**32)
    #compute offset and RTT
    rtt=(T4-T1)- (T3-T2)
    offset = ((T2-T1)+(T3-T4))/2
    
    return (rtt, offset)

def getCurrentTime(server="time.apple.com", port=123, iters=20) -> float:
   offsets = 0
   #get iters offsets
   for _ in range(iters):
       (pkt,T1,T4) = getNTPTimeValue(server, port)
       (RTT,offset) = ntpPktToRTTandOffset(pkt,T1,T4)  
       offsets+=offset
   data,T1,T4=getNTPTimeValue(server,port)
   t=struct.unpack("!12I",data)[10]
   #take average of offsets and add to current time
   currentTime=  t - TIME1970 +(offsets/iters)
   return currentTime


if __name__ == "__main__":

    print(getCurrentTime())
