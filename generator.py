import simpy
import random
import numpy as np
import networkx as nx
from edges import *



MTBA = 2
FLOWS = {}

class Generator:
    def __init__(self,net,env):
        self.net = net
        self.env = env

    def free(self,flow):
        for e in flow.path:
            e.load-=flow.bandwidth
        del FLOWS[flow.id]
    def flow_lifecycle(self,flow):
        yield self.env.timeout(self.env.now + flow.duration)
        self.free(flow)
        print(f"Flow {flow.id} deleted at time {self.env.now}")

    def flow_creation_cycle(self,edges):
        while True:
            yield self.env.timeout(np.random.exponential(MTBA))
            choice = np.random.choice(self.net.nodes,2,replace=False)
            gen = choice[0]
            sink = choice[1]
            path = nx.dijkstra_path(self.net,gen,sink)
            bw = np.random.randint(50,100)
            edgepath = []
            for i in range(0,len(path)-1):
                l = list(self.net[path[i]][path[i+1]])
                index = 0
                if len(l) > 1:
                    index = np.random.choice(range(0,len(l)))
                self.net[path[i]][path[i+1]][l[index]]["edge"].load += bw
                edgepath.append(self.net[path[i]][path[i+1]][l[index]]["edge"])
                if self.net[path[i]][path[i+1]][l[index]]["edge"].load > 1024:
            flow = Flow(bw,edgepath,gen,sink,np.random.randint(10,100),self.net,self.env)
            print(f"Flow {flow.id} created at time {self.env.now}")
            FLOWS[flow.id] = flow
            self.env.process(self.flow_lifecycle(flow))
            


            
            





