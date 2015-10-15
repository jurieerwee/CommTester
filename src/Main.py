'''
Created on 15 Oct 2015

@author: Jurie
'''

if __name__ == '__main__':
    pass

import socket
import json
import Tests
from io import StringIO






TCP_IP = '10.42.0.10'
TCP_PORT = 5000

BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

s.close()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

passed = Tests.test0(s)
print ('0: ' + str(passed))
if (passed == False):
    exit()

print ('1: ' + str(Tests.test1(s)))

print ('2: ' + str(Tests.test2(s)))

s.close()


