# bisimulation-checker
An algo for bisimulation of deterministic MSF.

PaigeAndTarjan algo implements the O(mlog(n)) algorithm to check if there exists a bisimulation.

PSEUDOCODE: \

A binary relation B subset of states[M1]xstates[M2] (where M1 and M2 are deterministic MSFs) is a bisimulation iff:\

1. initial_state of M1 and M2 are in B and \

2. for any state p,q of M1,M2 respectively: \
         if (p,q) are in B then: \ 
              for any input x of M1: \
                    output of (p,x) == output(q,x) and ( nextstate(p,x),nextstate(q,x) ) are in B \

Both files can be run as is on python 2.7. \

To shell: python __main__.py and follow the instructions to build the two MSF.
