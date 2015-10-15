import socket
import json

from io import StringIO
BUFFER_SIZE = 1024

def test0( s):
    io = StringIO()
    json.dump({'msg':{'id':0,'type':'stateCMD','instr':'prime'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    s.settimeout(2.0)
    try:
        s.recv(BUFFER_SIZE)
    except socket.timeout:
        return False
    
    return True

def test1( s):
    io = StringIO()     #Erroneous msg
    json.dump({'msg':{'ids':1,'type':'stateCMD','instr':'prime'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    
    io = StringIO()
    json.dump({'msg':{'id':2,'type':'stateCMD','instr':'prime'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    data = (s.recv(BUFFER_SIZE)).decode("utf-8").split('\n')[0]
    print (str.encode(data))
    reply = json.loads(data)#.decode("utf-8"))
    
    if(reply['reply']['id'] == 2):
        return True
    else:
        return False
    
def test2( s):
    msg = str.encode('{hadfgdfv}\n') 
    s.send(msg)
    
    io = StringIO()
    json.dump({'msg':{'id':3,'type':'stateCMD','instr':'prime'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    s.send(msg)
    data = s.recv(BUFFER_SIZE).decode("utf-8").split('\n')[0]
    reply = json.loads(data)
    print (data)
    if(reply['reply']['id'] == 3):
        return True
    else:
        return False
    
def test3( s):  #invalid type
    msg = str.encode('{hadfgdfv}\n') 
    s.send(msg)
    
    io = StringIO()
    json.dump({'msg':{'id':3,'type':'Blah','instr':'prime'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    s.send(msg)
    data = s.recv(BUFFER_SIZE).decode("utf-8").split('\n')[0]
    reply = json.loads(data)
    print (data)
    if(reply['reply']['id'] == 3):
        return True
    else:
        return False    