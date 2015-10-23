'''
Created on 15 Oct 2015

@author: Jurie
'''
#from _signal import CTRL_C_EVENT


if __name__ == '__main__':
    pass

import socket
import json
import Tests
from io import StringIO
import subprocess
import os
import time
from signal import SIGTERM

#os.system('cd ~/cpp_projects/RigController')
#if True:
with open("/home/jurie/cpp_projects/tests/outputs/test1.out","wb") as outputFile:
    p = subprocess.Popen(['sudo', '/home/jurie/cpp_projects/RigController/my_testRig','5000' ],cwd='/home/jurie/cpp_projects/RigController',stdout=outputFile)

    time.sleep(2)
    
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
    
    print ('3: ' + str(Tests.test3(s)))

    print ('4: ' + str(Tests.test4(s)))
    
    print ('5: ' + str(Tests.test5(s)))
    
    print ('6: ' + str(Tests.test6(s)))
    print ('7: ' + str(Tests.test7(s)))
    s.close()
    
    p.terminate()
    
    outputFile.close()

