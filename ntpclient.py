#!/usr/bin/env python

'''
CS352 Assignment 1: Network Time Protocol
You can work with 1 other CS352 student

DO NOT CHANGE ANY OF THE FUNCTION SIGNATURES BELOW
'''

from socket import socket, AF_INET, SOCK_DGRAM
import struct
from datetime import datetime


def getNTPTimeValue(server="time.apple.com", port=123) -> (bytes, float, float):
    # add your code here 
    client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(server, port)
    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    T1 = secs + float(time_difference.microseconds / 1000000.0)
    data = '\x1b'+47 * '\0'
    address = (server, port)
    client.sendto(data, address)
    data,address = client.recv(1024)
    #data is the packet
    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    T4= secs + float(time_difference.microseconds / 1000000.0)
    return (data, T1, T4)


def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    # add your code here 
    return (rtt, offset)

def getCurrentTime(server="time.apple.com", port=123, iters=20) -> float:
   data,T1,T4=getNTPTimeValue()
   t=struct.unpack("!12I",data)[10]
    
    return currentTime


if __name__ == "__main__":

    print(getCurrentTime())
