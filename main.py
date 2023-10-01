import simpy
import random
import networkx as nx
from generator import *
from edges import *
from solver import *
from metrichandler import * 


def parse(label):
    if label == "34 Mbps":
        return 34
    if label == "2.5 Gbps":
        return 2560
    if label == "100 Mbps":
        return 100
    if label == 'Peering, 2 Gbps':
        return 2048
    if label == "10 Gbps":
        return 10240
    if label == 'Fibre ottica spenta (Dark Fibre)' or label == 'Fibre ottica spenta (Dark Fibre), 10 Gbps':
        return 10240
    if label == 'Peering, 4Gbps':
        return 4096
    if label == 'Peering, 10 Gbps':
        return 10240
    if label == 'Peering, 13 Gbps':
        return 13312
    if label == 'Fibre ottica spenta (Dark Fibre), 20 Gbps':
        return 20480
    if label == '1 Gbps':
        return 1024
    if label == '622 Mbps':
        return 622
    if label == 'Peering, 5 Gbps':
        return 5120
    if label == 'Peering, 1 Gbps':
        return 1024

    return 1024
    
    
    

SOLVER = "FFDijkstra"
edges = {}
env = simpy.Environment()
net = nx.read_graphml("garr2011.graphml")
#nx.set_edge_attributes(net,Edge(5120),"edge")

visited = set()
for j in net.nodes:
    for k in net.nodes: 
        if net.has_edge(j,k):
            l = list(net[j][k])
            for q in range(0,len(l)):
                if (j,k,l[q]) not in visited:
                    try:
                        net[j][k][l[q]]["edge"] = Edge(parse(net[j][k][l[q]]["label"]),j,k,l[q])
                    except:
                        net[j][k][l[q]]["edge"] = Edge(1024,j,k,l[q])
                    visited.add((j,k,l[q]))
                    visited.add((k,j,l[q]))
                
                
    #edges[e[2]] = Edge(100)
metric = MetricHandler(net,env,SOLVER)
env.process(metric.printStats())
solver = None
if SOLVER == "FFDijkstra":
    solver = FFDijkstra(net,env,metric)
if SOLVER == "BFDijkstra":
    solver = BFDijkstra(net,env,metric)
if SOLVER == "WFDijkstra":
    solver = BFDijkstra(net,env,metric)
if solver == None:
    exit(-1)
generator = Generator(net,env,solver)
env.process(generator.flow_creation_cycle())
env.process(generator.migration_creation_cycle())

env.run(100000)



