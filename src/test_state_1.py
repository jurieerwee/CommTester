'''
Created on 21 Oct 2015

@author: Jurie
'''

''''
Tests the IDLE state.
Test that update returns 
*correct state
*correct valve state
*correct pumpRunning
*correct pressurised


'''

if __name__ == '__main__':
	pass

from TesterComms import TesterComms
import subprocess
import time
import sys

successfull = False
print ('State test1:')

debug = sys.argv[1]=='True'

with open("/home/jurie/cpp_projects/tests/outputs/test1.out","wb") as outputFile:
	p = subprocess.Popen(['sudo', '/home/jurie/cpp_projects/RigController/my_testRig','5000' ],cwd='/home/jurie/cpp_projects/RigController',stdout=outputFile)
	time.sleep(1)
	myComms = TesterComms()
	ids = 1
	obj = {"msg":{"id":ids,"type":"setCMD","instr":"activateUpdate"}}
	myComms.sendMsg(obj)
	time.sleep(1)
	reply = myComms.replyQ.get()
	if (reply['reply']['id']!= ids or reply['reply']['success']!= True or reply['reply']['code']!=1):
		print ('Reply Error')
	else:
	
		status = myComms.status
		print (status)
		if(status['update']['status']['state']!= 'IDLE'):
			successfull = False
		elif(status['update']['status']['inflowValve']!= False or status['update']['status']['outflowValve']!= False or status['update']['status']['releaseValve']!= False or status['update']['status']['pumpRunning']!= False):
			successfull = False	
		elif(status['update']['status']['pressurised']!= False):
			successfull = False
		else:
			successfull = True

	myComms.terminate = True
	
	p.terminate()

	outputFile.close()
	
	print (successfull)
	
	exit()
	
