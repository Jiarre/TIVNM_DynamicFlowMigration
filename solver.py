import networkx as nx
import numpy as np
from itertools import islice
import math
from copy import deepcopy as dc

class Solver:
    def __init__(self,net,env,metric):
        self.net = net
        self.env = env
        self.metric = metric
    
    def k_shortest_paths(self,G, source, target, k, weight=None):
        return list(
            islice(nx.shortest_simple_paths(G, source, target, weight=weight), k)
        )

    def r2c(self,generator,sink,edgepath):
        path = nx.dijkstra_path(self.net,generator,sink)
        self.metric.r2c.append(len(edgepath)/(len(path)-1))

    def saturation(self):
        visited = set()
        total_edges = len(self.net.edges)
        saturated_edges = 0
        for j in self.net.nodes:
            for k in self.net.nodes: 
                if self.net.has_edge(j,k):
                    l = list(self.net[j][k])
                    for q in range(0,len(l)):
                        if (j,k,l[q]) not in visited:
                            if self.net[j][k][l[q]]["edge"].load > self.net[j][k][l[q]]["edge"].bandwidth:
                                saturated_edges+=1
                            visited.add((j,k,l[q]))
                            visited.add((k,j,l[q]))
        
        print(saturated_edges/total_edges)
        self.metric.saturation.append(saturated_edges/total_edges)
    
    def path(self,generator,sink,bw):
        path = nx.dijkstra_path(self.net,generator,sink)
        edgepath = []
        for i in range(0,len(path)-1):
            l = list(self.net[path[i]][path[i+1]])
            index = 0
            if len(l) > 1:
                index = np.random.choice(range(0,len(l)))
            kok = self.net[path[i]][path[i+1]][l[index]]["edge"]
            
            self.net[path[i]][path[i+1]][l[index]]["edge"].load += bw
            #print(f"Edge {kok.id} load {kok.load-bw}-> {kok.load}  (bw req of {bw})")
            edgepath.append(self.net[path[i]][path[i+1]][l[index]]["edge"])
        self.r2c(generator,sink,edgepath)
        self.saturation()
        return edgepath

    def extract(self,edge,flow):
        edge.load -= flow.bandwidth
        

    

    
class FFDijkstra(Solver):

    def __init__(self,net,env,metric):
        Solver.__init__(self,net,env,metric)

    def flow_remap(self,flow,to_remap):
        tempnet = nx.MultiGraph(self.net)
        for j in self.net.nodes:
            for k in self.net.nodes: 
                if self.net.has_edge(j,k):
                    l = list(self.net[j][k])
                    if len(l)>1:
                        for q in range(0,len(l)):
                            if flow in self.net[j][k][l[q]]["edge"].flows:
                                try:
                                    dummy = nx.MultiGraph(tempnet)
                                    dummy.remove_edge(j,k,key=l[q])
                                    if nx.is_connected(dummy):
                                        tempnet = dummy
                                    
                                except:
                                    continue
        for f in to_remap:   
            for e in f.path:
                e.flows.remove(f)
                e.load -= f.bandwidth
            old_path = f.path                
            path = nx.dijkstra_path(tempnet,f.source,f.destination)
            edgepath = []
            for i in range(0,len(path)-1):
                l = list(self.net[path[i]][path[i+1]])
                index = 0
                if len(l) > 1:
                    index = np.random.choice(range(0,len(l)))
                kok = self.net[path[i]][path[i+1]][l[index]]["edge"]
                self.net[path[i]][path[i+1]][l[index]]["edge"].load += f.bandwidth
                #print(f"MIGRATION Edge {kok.id} load {kok.load-f.bandwidth}-> {kok.load}  (bw req of {f.bandwidth})")

                edgepath.append(self.net[path[i]][path[i+1]][l[index]]["edge"])
            #self.r2c(generator,sink,edgepath)
            #self.saturation()
            for e in edgepath:
                e.flows.append(f)
            f.path = edgepath
            #print(f"Flow {f.id} remapped from {old_path} to {edgepath}")   

class BFDijkstra(Solver):

    def __init__(self,net,env,metric):
        Solver.__init__(self,net,env,metric)

    

class WFDijkstra(Solver):

    def __init__(self,net,env,metric):
        Solver.__init__(self,net,env,metric)

    """def path(self,generator,sink,bw):
        #paths = list(nx.all_simple_paths(self.net, generator, sink))
        path = nx.dijkstra_path(self.net,generator,sink)
        edgepath = []
        for i in range(0,len(path)-1):
            l = list(self.net[path[i]][path[i+1]])
            index = 0
            if len(l) > 1:
                index = 0
                best_distance = 0
                for k in range(0,len(l)):
                    tmp = abs(self.net[path[i]][path[i+1]][l[k]]["edge"].bandwidth - (self.net[path[i]][path[i+1]][l[k]]["edge"].load+bw)) 
                    if tmp > best_distance:
                        best_distance = tmp
                        index = k
            self.net[path[i]][path[i+1]][l[index]]["edge"].load += bw
            edgepath.append(self.net[path[i]][path[i+1]][l[index]]["edge"]) 
        self.r2c(generator,sink,edgepath)
        self.saturation()
        return edgepath"""