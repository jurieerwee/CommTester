'''
Created on 24 Oct 2015

@author: Jurie
'''

import subprocess

for i in range (0,20):
	p = subprocess.Popen(['sudo', 'python3', './src/test_state_'+str(i)+'.py', 'False'])
	p.wait()
