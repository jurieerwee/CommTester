'''
Created on 21 Oct 2015

@author: Jurie
'''
import time
import subprocess
import sys

terminate = False

def flowSim(direction, pulse_per_sec):
	global terminate
	subprocess.Popen(['gpio', 'mode','2', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
	if (direction == True):
		subprocess.Popen(['gpio', 'mode','2', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
	else:
		subprocess.Popen(['gpio', 'mode','2', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
	
	while(terminate==False):
		subprocess.Popen(['gpio', 'mode','3', 'up' ],cwd='/home/jurie/cpp_projects/RigController')
		time.sleep(1/pulse_per_sec/2)
		subprocess.Popen(['gpio', 'mode','3', 'down' ],cwd='/home/jurie/cpp_projects/RigController')
		time.sleep(1/pulse_per_sec/2)