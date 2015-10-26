'''
Created on 21 Oct 2015

@author: Jurie
'''
import socket
import json
import queue
from io import StringIO
import threading
import time
import select

class TesterComms(object):

	#@staticmethod	
	def recvThread(self):
		start = time.time()
		while(self.terminate == False):
			if(time.time()-start > 1):
				print("More than second since last update")
			ready = select.select([self.s],[],[])
			if(ready):
				
				data = (self.s.recv(self.BUFFER_SIZE)).decode("utf-8").split('\n')[0]
				try:
					message = json.loads(data)
					key = next(iter(message.keys()))
					if( key== 'reply'):
						self.replyQ.put(message)
						#print ("Received reply")
					elif(key == 'update'):
						self.status = message	
						start = time.time()
				except ValueError as e:
					print(e)
					print(data)
	
	
	def __init__(self):
		TCP_IP = '127.0.0.1'
		TCP_PORT = 5000
		self.BUFFER_SIZE = 1024
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.connect((TCP_IP,TCP_PORT))
		
		self.terminate = False
		self.status = {}
		
		self.replyQ = queue.Queue(10)
		t_recv = threading.Thread(target=self.recvThread)
		t_recv.start()
		
	
				
	def sendMsg(self, obj):
		io = StringIO()     #Erroneous msg
		json.dump(obj,io)
		msg = str.encode(io.getvalue()+ '\n') 
		#print ("Sending: " + io.getvalue())
		self.s.send(msg)
		
#myComms = TesterComms()

#obj = {"msg":{"id":1,"type":"setCMD","instr":"activateUpdate"}}
#myComms.sendMsg(obj)

#time.sleep(1)
#print (myComms.replyQ.get())
#print( myComms.status)

#obj = {"msg":{"id":2,"type":"stateCMD","instr":"startPump"}}
#myComms.sendMsg(obj)

#time.sleep(1)
#print (myComms.replyQ.get())
#print( myComms.status)

