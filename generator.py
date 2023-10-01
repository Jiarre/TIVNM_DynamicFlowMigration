import simpy
import random
import numpy as np
import networkx as nx
from edges import *



MTBA = 2
MTBE = 50
FLOWS = {}

class Generator:
    def __init__(self,net,env,solver):
        self.net = net
        self.env = env
        self.solver = solver
    def integrationTest(self,flow):
        edges = [flow.path]
        edgepath = flow.path
        visited = set()
        for e in edgepath:
            if flow not in e.flows:
                print("Flow not present in edge path")
                exit(-1)
            pload = e.load
            for f in e.flows:
                pload-=f.bandwidth
            if pload != 0:
                print(f"Mismatch in edge {e.id}, got {pload}")
                exit(-1)
        for j in self.net.nodes:
            for k in self.net.nodes: 
                if self.net.has_edge(j,k):
                    l = list(self.net[j][k])
                    for q in range(0,len(l)):
                        if flow in self.net[j][k][l[q]]["edge"].flows and self.net[j][k][l[q]]["edge"] not in edgepath:
                            print("Edge contains flow")
                            exit(-1)

        #print(f"Deleting {flow.id}, {len(list(FLOWS.keys()))} active flows ")
        
    def free(self,flow):
        for e in flow.path:
            e.load-=flow.bandwidth
            e.flows.remove(flow)
        del FLOWS[flow.id]

    def flow_lifecycle(self,flow):
        yield self.env.timeout(flow.duration)
        self.integrationTest(flow)
        self.free(flow)
        #print(f"Flow {flow.id} deleted at time {self.env.now}")

    def flow_creation_cycle(self):
    
        while True:
            yield self.env.timeout(np.random.exponential(MTBA))
            choice = np.random.choice(self.net.nodes,2,replace=False)
            gen = choice[0]
            sink = choice[1]
            bw = np.random.randint(10,1024)
            duration = np.random.randint(MTBA,50)
            edgepath = self.solver.path(gen,sink,bw)
            flow = Flow(bw,edgepath,gen,sink,duration,self.net,self.env)
            for e in edgepath:
                e.flows.append(flow)
            FLOWS[flow.id] = flow
            self.env.process(self.flow_lifecycle(flow))
    
    def migration_creation_cycle(self):

        while True:
            yield self.env.timeout(np.random.exponential(MTBA))
            try:
                flow_choice = np.random.choice(list(FLOWS.keys()))
                flow = FLOWS[flow_choice]
                #print(f"Flow {flow.id} chosen")
            except:
                continue
            
            edges = flow.path
            to_remap = []
            for e in edges:
                for f in e.flows:
                    #print(f.id)
                    if f != flow and f not in to_remap:
                        to_remap.append(f)
            #print(FLOWS.keys())
            #print([f.id for f in to_remap])
            self.solver.flow_remap(flow,to_remap)
            
           


            
            





