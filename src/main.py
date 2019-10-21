import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

import PaigeAndTarjan as PT

#m1=nx.DiGraph();

#m1.add_edge(0,1,action=1)
#m1.add_edge(1,2,action=2)
#m1.add_edge(0,2,action=1)
#m1.add_edge(2,2,action=2)
#actions = [1,2]

#m2 = nx.DiGraph()
#m2.add_edge(0,1,action=1)
#m2.add_edge(1,1,action=2)
#actions2=[1,2]

check=1;#begin

while(check!=0):
	edge = tuple(raw_input("give first of edge (fromto):"));
	io = input("give action value for this transition:"); 
	if(len(edge)==2 and len(io)==1):	
		m1.add_edge(edge[0],edge[1],label=io);
		print("saved")
	else:
		print("error")
		exit(1)
	check=input("finish (0 to end):");

m2=nx.DiGraph();

check=1 #restart

while(check!=0):
	edge = tuple(raw_input("give first of edge (fromto):"));
	io = input("give action value for this transition:"); 
	if(len(edge)==2 and len(io)==1):	
		m2.add_edge(edge[0],edge[1],label=io);
		print("saved")
	else:
		print("error")
		exit(1)
	check=input("finish (0 to end):");

print("GIVE SET OF ACTIONS OF M1");
actions=[];
check=1
while(check):
	a = input("action value:")
	actions.append(a)
	check=input("finish (o to end)");

actions2=[]

print("GIVE SET OF ACTIONS OF M2");
check=1
while(check):
	a = input("action value:")
	actions.append(a)
	check=input("finish (o to end)");


k = PT.PaigeAndTarjan(actions)
print(k.isBisimilar(m1,m2))

Q = nx.disjoint_union_all([m1,m2])
k.getCoarsestPartition(Q, plot=True)




