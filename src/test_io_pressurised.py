'''
Created on 23 Oct 2015

@author: Jurie
'''

''''
Tests the pressured flag.
**Set pressure**
Assumed threashhold pressure is 1.5
Test that the pressurised flags gets set and unset.
'''

if __name__ == '__main__':
	pass

from TesterComms import TesterComms
import subprocess
import time
import sys
import threading
import flowSim
debug = False
try:
	debug = sys.argv[1]=='True' or sys.argv[1]=='debug'
except IndexError as e:
	debug = False

successfull = False
print (sys.argv[0])

with open("/home/jurie/cpp_projects/tests/outputs/state_test2.out","wb") as outputFile:
	p = subprocess.Popen(['sudo', '/home/jurie/cpp_projects/RigController/my_testRig','5000' ],cwd='/home/jurie/cpp_projects/RigController',stdout=outputFile)
	time.sleep(1)
	while True:
		try:
			myComms = TesterComms()
			ids = 0
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":0.0}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			if debug:
				print(reply)
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error1')
				break
			
			ids +=1	
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"activatePressureOverrideCMD"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error2')
				break
			
			ids+=1	
			obj = {"msg":{"id":ids,"type":"setCMD","instr":"activateUpdate"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error3')
				break
			time.sleep(2)
			
			status = myComms.status
			if(debug):
				print (status)
			if(status['update']['status']['pressurised']!= False):
				successfull = False
				break
			
			ids+=1	
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":2.0}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			if debug:
				print(reply)
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error1')
				break
			
			time.sleep(2)
			
			status = myComms.status
			if(debug):
				print (status)
			if(status['update']['status']['pressurised']!= True):
				successfull = False
				break
			
			ids+=1	
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":1.0}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			if debug:
				print(reply)
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error1')
				break
			
			time.sleep(1)
			
			status = myComms.status
			if(debug):
				print (status)
			if(status['update']['status']['pressurised']!= False):
				successfull = False
				break
			else:
				successfull = True
			
			
				
			

			break		
		except KeyError as e:
			print(e)
			break
	
	flowSim.terminate = True
	
	myComms.terminate = True
	
	p.terminate()

	outputFile.close()
	
	print (successfull)
	
	exit()
	
