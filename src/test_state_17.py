'''
Created on 21 Oct 2015

@author: Jurie
'''

''''
Tests the PRIME state sequence, only continuing to Prime4 after tankTransient and terminating with IDLE request
**Set pressure**
**Simualte reverse flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Dependent on test3 and test4 passing




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
			
			#simulate empty tank
			subprocess.Popen(['gpio', 'mode','0', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
			subprocess.Popen(['gpio', 'mode','1', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
			
			ids = 0
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":2.0}}
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
			obj = {"msg":{"id":ids,"type":"stateCMD","instr":"prime"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get()
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error')
				break
			
			count = 10
			while(myComms.status['update']['status']['state']!= 'PRIME1' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['state'])
			if(count ==0):
				successfull = False
				break
			
			t_flowSim = threading.Thread(target=flowSim.flowSim,args=(False,10))
			t_flowSim.start()
			
			count = 11
			while(myComms.status['update']['status']['state']!= 'PRIME2' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update'])
			if(count ==0):
				successfull = False
				break
			
			count = 11
			while(myComms.status['update']['status']['state']!= 'PRIME3' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['state'])
			if(count ==0):
				successfull = False
				break
			
			#Stay within Prime3 for 30 seconds
			count = 30
			while(myComms.status['update']['status']['state']== 'PRIME3' and count >0):
				time.sleep(1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['state'])
			
			if(myComms.status['update']['status']['state']!= 'PRIME3'):
				successfull = False
				break
			
			#simulate transient tank
			subprocess.Popen(['gpio', 'mode','0', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
			subprocess.Popen(['gpio', 'mode','1', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
			
			count = 15
			while(myComms.status['update']['status']['state']!= 'PRIME4' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['state'],myComms.status['update']['status']['tank'])
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
	
