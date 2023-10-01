import simpy
import random
from generator import *


ID=0
class Edge:

    def __init__(self,bw,n1,n2,id):
        self.n1 = n1
        self.n2 = n2
        self.id = id
        self.bandwidth = bw
        self.load = 0
        self.flows = []
    

class Flow:


    def __init__(self,bw,path,source,destination,duration,net,env):
        global ID
        self.id = ID
        ID+=1
        self.duration = duration
        self.bandwidth = bw
        self.path = path
        self.source = source
        self.destination = destination
    
    

    
            