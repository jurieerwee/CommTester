'''
Created on 21 Oct 2015

@author: Jurie
'''

''''
Tests the PUMPING state enters .
**Set pressure**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Dependent on test3 passing




'''

if __name__ == '__main__':
	pass

from TesterComms import TesterComms
import subprocess
import time
import sys

debug = False
try:
	debug = sys.argv[1]=='True' or sys.argv[1]=='debug'
except IndexError as e:
	debug = False

successfull = False
print ('State test8:')

with open("/home/jurie/cpp_projects/tests/outputs/state_test2.out","wb") as outputFile:
	p = subprocess.Popen(['sudo', '/home/jurie/cpp_projects/RigController/my_testRig','5000' ],cwd='/home/jurie/cpp_projects/RigController',stdout=outputFile)
	time.sleep(1)
	while True:
		try:
			myComms = TesterComms()
			ids = 0
			#simulate no pump Error and pump not running (NC)
			subprocess.Popen(['gpio', 'mode','25', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
			subprocess.Popen(['gpio', 'mode','29', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
			# low pressure >> no pressure
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":0.5}}
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
			
			#TankFull
			subprocess.Popen(['gpio', 'mode','1', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
			subprocess.Popen(['gpio', 'mode','0', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
			
			#pumpNotRunning
			subprocess.Popen(['gpio', 'mode','29', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
			#noPumpErrer
			subprocess.Popen(['gpio', 'mode','25', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
			
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
			if(status['update']['status']['state']!= 'IDLE'):
				successfull = False
				break
			
			ids+=1	
			obj = {"msg":{"id":ids,"type":"stateCMD","instr":"startPump"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get()
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error')
				break
			
			if(debug):
				print('startPump command successfull', reply)
				
			#simulate pumpStart
			subprocess.Popen(['gpio', 'mode','29', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
			# high pressure >> pressure
			obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":3.5}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			if debug:
				print(reply)
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error')
				break
			
			time.sleep(1.1)
			count = 20
			while(myComms.status['update']['status']['state']!= 'PUMPING' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update'])
			if(count ==0):
				successfull = False
				break
			else:
				successfull = True

			break		
		except KeyError as e:
			print(e)
			break
	
	#simulate tri
	subprocess.Popen(['gpio', 'mode','29', 'tri' ],cwd='/home/jurie/cpp_projects/RigController')
	myComms.terminate = True
	
	p.terminate()

	outputFile.close()
	
	print (successfull)
	
	exit()
	
