
import flowSim
import time
import threading

t_recv = threading.Thread(target=flowSim.flowSim,args=(True,2))
t_recv.start()

time.sleep(30)


flowSim.terminate = True
