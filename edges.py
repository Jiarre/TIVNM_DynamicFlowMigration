import simpy
import random
from generator import *


ID=0
class Edge:
    def __init__(self,bw):
        self.bandwidth = bw
        self.load = 0
    def __str__(self):
        return f'total bw: {self.bandwidth}, used: {self.load}'

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
    
    

    
            