import simpy
import random
import networkx as nx
from generator import *
from edges import *

edges = {}
env = simpy.Environment()
net = nx.read_graphml("garr2011.graphml")
#nx.set_edge_attributes(net,Edge(5120),"edge")

for j in net.nodes:
    for k in net.nodes: 
        if net.has_edge(j,k):
            l = list(net[j][k])
            for q in range(0,len(l)):
                net[j][k][l[q]]["edge"] = Edge(1024)
    #edges[e[2]] = Edge(100)
generator = Generator(net,env)
env.process(generator.flow_creation_cycle(edges))
env.run(1000)



