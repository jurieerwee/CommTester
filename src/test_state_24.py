'''
Created on 26 Oct 2015

@author: Jurie
'''

''''
Tests OVERRIDE state enters from IDLE_PRES

Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence
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
	#simulate trans tank
	subprocess.Popen(['gpio', 'mode','0', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
	subprocess.Popen(['gpio', 'mode','1', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
	
	while True:
		try:
			myComms = TesterComms()
			ids = 0
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":3.0}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			if debug:
				print(reply)
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error')
				break
			
			ids +=1	
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"activatePressureOverrideCMD"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error')
				break
			
			ids+=1	
			obj = {"msg":{"id":ids,"type":"setCMD","instr":"activateUpdate"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error')
				break
			time.sleep(1)
			
			status = myComms.status
			if(debug):
				print (status)
			if(status['update']['status']['state']!= 'IDLE_PRES'):
				successfull = False
				break
			
			ids+=1	
			obj = {"msg":{"id":ids,"type":"stateCMD","instr":"override"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get()
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error on override')
				break
			
			count = 10
			while(myComms.status['update']['status']['state']!= 'OVERRIDE' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['state'])
			if(count ==0):
				successfull = False
				break
			
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
	
