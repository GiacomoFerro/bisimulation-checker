import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

class PaigeAndTarjan:
    def __init__(self, actions):
        self.actions = actions

    # computes the pre.
    # S is an array of nodes.
    def pre(self,S,Q,a=None):
        pre = []
        for node in Q.nodes():
            neighbors = Q.neighbors(node)
            if a != None:
                if any((neighbor in S and Q[node][neighbor]["action"]==a) for neighbor in neighbors):
                    pre.append(node)
            elif any((neighbor in S) for neighbor in neighbors):
                pre.append(node)
        return set(pre)

    def getInitialRefinement(self, Q):
        B1 = set(self.pre(Q.nodes(),Q))
        B2 = set(Q.nodes()) - set(B1)
        if not (B1==set([]) or B2==set([])):
            return [B1, B2]
        for action in self.actions:
            B1 = set(self.pre(Q.nodes(),Q, action))
            B2 = set(Q.nodes()) - set(B1)
            if not (B1==set([]) or B2==set([])):
                return [B1, B2]
        
    # Both B and S are assumed to be lists of nodes
    # These are both sets.
    def setIsStableWRTSet(self, B, S):
        if not any(b in self.pre(S, Q) for b in B):
            return True
        if B in S:
            return True
        return False
        
    # This is assumed to be a group of blocks (or sets)
    def partitionIsStableWRTSet(self, pi, S):
        if all(self.setIsStableWRTSet(B, S) for B in pi):
            return True
        return False

    # This is two groups of blocks
    def partitionIsStableWRTPartition(self, pi, piPrime):
        if all(self.partitionIsStableWRTSet(self, pi, S) for S in piPrime):
            return True
        return False

    def partitionIsStable(self, pi):
        return partitionIsStableWRTPartition(self, pi, pi) 

    def refineOnSet(self, B, S):
        B1 = set(B).intersection(set(pre(S, Q)))
        B2 = set(B)-set(pre(S, Q))
        return [B1, B2]

    def refinePartitionOnSet(self, preB, pi):
        piPrime = []
        for D in pi:
            D1 = D.intersect(preB)
            D2 = D-D1
            if(D1 != [] and D2 != []):
                piPrime.append([D1, D2])
            if(D1 != [] and D2 == []):
                piPrime.append([D1])
            if(D1 == [] and D2 != []):
                piPrime.append([D2])
        return piPrime

    # implements split(S\B, split(B,pi))
    def threeWayRefinement(self, S, B, pi, Q):
        preB = self.pre(B, Q)
        preSminusB = self.pre(S-B, Q)

        piPrime = []
        for D in pi:
            D2 = set(D)-preB
            if D2 != set([]) and D2 not in piPrime: piPrime.append(D2)
            D11 = D.intersection(preB).intersection(preSminusB)
            if D11 != set([]) and D11 not in piPrime: piPrime.append(D11)
            D12 = D - preSminusB
            if D12 != set([]) and D12 not in piPrime: piPrime.append(D12)
        return piPrime

    def getDesiredBlockFromCompound(self, S, pi):
        blocksOfInterest = []
        i = 0
        for block in pi:
            if block.issubset(S):
                blocksOfInterest.append(block)
                i += 1
            if i==2:
                if(blocksOfInterest[0]<=blocksOfInterest[1]):
                    return blocksOfInterest[0]
                else:
                    return blocksOfInterest[1]
        return False

    def recreateC(self, pi, X):
        C = []
        for x in X:
            i=0
            for p in pi:
                if p.issubset(x):
                    i+=1
                if i==2:
                    C.append(x)
                    break
        return C

    def getCoarsestPartition(self,Q, plot=False):
        # Preprocessing step
        # Initial values
        pi = self.getInitialRefinement(Q)
        X = [set(Q.nodes())]
        C = [set(Q.nodes())]
        
        pos = nx.spring_layout(Q)

        # Now loop:
        while len(pi)!=len(X):
            # Step 1:
            # Use a heuristic to find a value for B that is reasonable.
            C = self.recreateC(pi,X)
            S = C.pop()
            B = self.getDesiredBlockFromCompound(S, pi)

            # Step 2:
            # update X:
            X.remove(S)
            X.append(S-B)
            X.append(B)
            if(self.getDesiredBlockFromCompound(S-B, pi) != False):
                C.append(S)
            
            # Step 3:
            # Compute the pre(B):
            # (Maybe come back and compute count)
            preB = self.pre(B, Q)

            # Step 4:
            pi = self.threeWayRefinement(S, B, pi, Q)
            if plot:
                self.plotGraph(pi, Q, pos)
        return pi

    # This plots the graph. The arrows are color coded according to action
    # and the nodes are color coded according to partition. The partition value
    # will depend on the global variable. Initially, there will be only one
    # partition and all the nodes will have the same color.
    def plotGraph(self, blocks, Q, pos=None):
        numOfActions = len(self.actions)
        numOfBlocks = len(blocks)

        plt.figure(1)
        if not pos:
            pos = nx.spring_layout(Q)
        nodeColors = cm.rainbow(np.linspace(0,1,numOfBlocks))
        edgeColors = cm.rainbow(np.linspace(0,1,numOfActions))
        for i in xrange(len(blocks)):
            nx.draw_networkx_nodes(Q,pos,nodelist=blocks[i],node_color=nodeColors[i])
        for i in xrange(numOfActions):
            acts = []
            for edge in Q.edges():
                if(Q.get_edge_data(*edge)["action"]==self.actions[i]):
                    acts.append(edge)
            nx.draw_networkx_edges(Q,pos,edgelist=acts,edge_color=[edgeColors[i]]*len(acts))
        plt.show()

    # This verifies that the two graphs are bisimilar.
    def isBisimilar(self, Q1, Q2):
        Q = nx.union_all([Q1,Q2], rename=('G-', 'H-'))
        blocks = self.getCoarsestPartition(Q)
        # Confirms that there is at least one of each type of node in each partition.
        # If there is, we have bisimilarity. Otherwise, we don't.
        for block in blocks:
            if not any('H' in nodeName for nodeName in block):
                return False
            if not any('G' in nodeName for nodeName in block):
                return False
        return True
