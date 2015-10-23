import socket
import json

from io import StringIO
BUFFER_SIZE = 1024

def test0( s):
    io = StringIO()
    obj = {'msg':{'id':0,'type':'stateCMD','instr':'prime'}}
    print(type(obj))
    print(type(io))
    json.dump(obj,io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    s.settimeout(10.0)
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
    
def test4( s):
    io = StringIO()     #type spelt wrong
    json.dump({'msg':{'id':10,'trype':'stateCMD','instr':'prime'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    
    data = (s.recv(BUFFER_SIZE)).decode("utf-8").split('\n')[0]
    print (str.encode(data))
    reply = json.loads(data)#.decode("utf-8"))
    
    if(reply['reply']['id'] == 10 and reply['reply']['success']==False):
        return True
    else:
        return False
    
def test5( s):
    io = StringIO()     #instr spelt wrong
    json.dump({'msg':{'id':11,'type':'stateCMD','instruct':'prime'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    
    data = (s.recv(BUFFER_SIZE)).decode("utf-8").split('\n')[0]
    print (str.encode(data))
    reply = json.loads(data)#.decode("utf-8"))
    
    if(reply['reply']['id'] == 11 and reply['reply']['success']==False):
        return True
    else:
        return False
       
def test6( s):
    io = StringIO()     #invalid instruction at stateCMD
    json.dump({'msg':{'id':12,'type':'stateCMD','instr':'drfgd'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    
    data = (s.recv(BUFFER_SIZE)).decode("utf-8").split('\n')[0]
    print (str.encode(data))
    reply = json.loads(data)#.decode("utf-8"))
    
    if(reply['reply']['id'] == 12 and reply['reply']['success']==False):
        return True
    else:
        return False
       

       
def test7( s):
    io = StringIO()     #invalid instruction at setCMD
    json.dump({'msg':{'id':12,'type':'setCMD','instr':'drfgd'}},io)
    msg = str.encode(io.getvalue()+ '\n') 
    print ("Sending: " + io.getvalue())
    s.send(msg)
    
    data = (s.recv(BUFFER_SIZE)).decode("utf-8").split('\n')[0]
    print (str.encode(data))
    reply = json.loads(data)#.decode("utf-8"))
    
    if(reply['reply']['id'] == 12 and reply['reply']['success']==False):
        return True
    else:
        return False