'''
Created on 21 Oct 2015

@author: Jurie
'''

''''
Tests the PRIME state sequence, termimating with tankFull.
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
print ('State test7:')

with open("/home/jurie/cpp_projects/tests/outputs/state_test2.out","wb") as outputFile:
	p = subprocess.Popen(['sudo', '/home/jurie/cpp_projects/RigController/my_testRig','5000' ],cwd='/home/jurie/cpp_projects/RigController',stdout=outputFile)
	time.sleep(1)
	while True:
		try:
			myComms = TesterComms()
			ids = 0
			
			obj = {"msg":{"id":ids,"type":"setCMD","instr":"activateUpdate"}}
			myComms.sendMsg(obj)
			reply = myComms.replyQ.get(block=True,timeout=1)
			
			if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
				print ('Reply Error')
				break
			time.sleep(1)
			
			#simulate tankTransient
			gpio= subprocess.Popen(['gpio', 'mode','0', 'up' ],cwd='/home/jurie/cpp_projects/RigController') #FullPin
			gpio.wait()
			gpio= subprocess.Popen(['gpio', 'mode','1', 'up' ],cwd='/home/jurie/cpp_projects/RigController') #EmptyPin
			gpio.wait()
			count = 10
			while(myComms.status['update']['status']['tank']!= 'TRANSIENT' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['tank'])
			if(count ==0):
				successfull = False
				break
				
			print("Transient passed")
				
			#simulate tankEmpty
			gpio=subprocess.Popen(['gpio', 'mode','0', 'up' ],cwd='/home/jurie/cpp_projects/RigController') #FullPin
			gpio.wait()
			gpio=subprocess.Popen(['gpio', 'mode','1', 'down' ],cwd='/home/jurie/cpp_projects/RigController') #EmptyPin
			gpio.wait()
			
			count = 10
			while(myComms.status['update']['status']['tank']!= 'EMPTY' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['tank'])
			if(count ==0):
				successfull = False
				break
			
			print("Empty passed")
				
			#simulate tankFull
			gpio=subprocess.Popen(['gpio', 'mode','0', 'down' ],cwd='/home/jurie/cpp_projects/RigController') #FullPin
			gpio.wait()
			gpio=subprocess.Popen(['gpio', 'mode','1', 'up' ],cwd='/home/jurie/cpp_projects/RigController') #EmptyPin
			gpio.wait()
			
			count = 10
			while(myComms.status['update']['status']['tank']!= 'EMPTY' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['tank'])
			if(count ==0):
				successfull = False
				break
			
			print("Full passed")
				
			#simulate tankERROR
			gpio=subprocess.Popen(['gpio', 'mode','0', 'down' ],cwd='/home/jurie/cpp_projects/RigController') #FullPin
			gpio.wait()
			gpio=subprocess.Popen(['gpio', 'mode','1', 'down' ],cwd='/home/jurie/cpp_projects/RigController') #EmptyPin
			gpio.wait()
			
			count = 10
			while(myComms.status['update']['status']['tank']!= 'TANK_ERROR' and count >0):
				time.sleep(0.1)
				count -=1
				if(debug):
					print(myComms.status['update']['status']['tank'])
			if(count ==0):
				successfull = False
				break
			
			print("Error passed")
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
	
