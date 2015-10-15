"""Implements broadcast and convergecast on a tree topology."""
# In the whole file port 0 is assumed to be the parent.

from random import shuffle
from da import Node, Network
import topo

################################################################################

class Broadcast(Node):
    def run(self):
        self.data['msg'] = None
        if 'shout' in self.data: self.send(0, ('dispatch', self.data['shout']))
        while True:
            p, m = self.recv()
            if m[0] == 'dispatch' and p == 0:
                self.data['msg'] = m[1]
                for p in range(1, self.deg):
                    self.send(p, ('dispatch', self.data['msg']))
                return

def run_broadcast(t):
    print('--- running broadcast ---')
    msg = 'test'
    net = Network(Broadcast, t)
    net.nodes[0].data['shout'] = msg  # this one will initiate the shout
    net.run()
    
    # check that it worked
    for n in net.nodes:
        if n.data['msg'] != msg:
            n.log('did not receive message!')

################################################################################

class Convergecast(Node):
    def run(self):
        self.data['max'] = self.data['msg']
        cnt = 0
        while True:
            if cnt == self.deg - 1:
                self.send(0, ('my max', self.data['max']))
                return
            p, m = self.recv()
            if m[0] == 'my max':
                self.data['max'] = max(self.data['max'], m[1])
                cnt += 1

def run_convergecast(t):
    print('--- running convergecast ---')
    net = Network(Convergecast, t)
    msgs = list(range(100)); shuffle(msgs)
    for n, m in zip(net.nodes, msgs): n.data['msg'] = m
    net.run()

    # check that it worked
    m = max([ n.data['msg'] for n in net.nodes ])
    k = net.nodes[0].data['max']
    if k != m: print('Found {}, but max is {}!', k, m)

################################################################################

parents = [0, 6, 0, 2, 5, 6, 0]  # 0 is its own parent -- root
t = topo.bidirectional({ i: [p] for i, p in enumerate(parents) })

if __name__ == '__main__':
    run_broadcast(t)
    run_convergecast(t)
