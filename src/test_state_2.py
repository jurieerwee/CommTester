'''
Created on 21 Oct 2015

@author: Jurie
'''

''''
Tests the tester pressureOverride


'''

if __name__ == '__main__':
	pass

from TesterComms import TesterComms
import subprocess
import time
import sys

debug = sys.argv[1]=='True'

successfull = False
print ('State test2:')

with open("/home/jurie/cpp_projects/tests/outputs/state_test2.out","wb") as outputFile:
	p = subprocess.Popen(['sudo', '/home/jurie/cpp_projects/RigController/my_testRig','5000' ],cwd='/home/jurie/cpp_projects/RigController',stdout=outputFile)
	time.sleep(1)
	try:
		myComms = TesterComms()
		ids = 0
		obj = {"msg":{"id":ids,"type":"testerCMD","instr":"setPressureCMD","pressure":2.0}}
		myComms.sendMsg(obj)
		time.sleep(1)
		reply = myComms.replyQ.get()
		if debug:
			print(reply)
		if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
			print ('Reply Error')
		
		ids +=1	
		obj = {"msg":{"id":ids,"type":"testerCMD","instr":"activatePressureOverrideCMD"}}
		myComms.sendMsg(obj)
		time.sleep(1)
		reply = myComms.replyQ.get()
		if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
			print ('Reply Error')
		
		ids+=1	
		obj = {"msg":{"id":ids,"type":"setCMD","instr":"activateUpdate"}}
		myComms.sendMsg(obj)
		time.sleep(1)
		reply = myComms.replyQ.get()
		
		if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
			print ('Reply Error')
		else:
		
			status = myComms.status
			if(status['update']['runningData']['pressure']!=2.0):
				successfull = False
			else:
				successfull = True
	except KeyError as e:
		print(e)
	
	myComms.terminate = True
	
	p.terminate()

	outputFile.close()
	
	print (successfull)
	
	exit()
	
