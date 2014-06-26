#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket
import time
number = 23
running = True
for i in range(1, 10):
    HOST = '192.168.79.253' # The remote host
    #HOST = '192.168.76.61' # The remote host
    PORT = 2425 # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
    s.connect((HOST, PORT))
    s.send('1_lbt4_35#128#0022680C51AC#0#35807#0:1250815230:胡波_PC:testHUBO-PC64:209:')
    i = i + 1
    #time.sleep(1*2) 
s.close()
