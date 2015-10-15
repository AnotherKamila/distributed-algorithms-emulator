"""Implements a shout-and-echo algorithm on any topology."""

from da import Node, Network
import topo

class ShoutAndEcho(Node):
    def run(self):
        marked_edges = [ False for e in range(self.deg) ]
        first_from = None

        if 'shout' in self.data:
            self.data['msg'] = self.data['shout']
            for p in range(self.deg): self.send(p, ('shout', self.data['msg']))

        while True:
            if all(marked_edges):
                if 'shout' not in self.data:
                    self.send(first_from, ('echo', self.data['msg']))
                return
            p, m = self.recv()
            if m[0] == 'echo': marked_edges[p] = True
            if m[0] == 'shout':
                if 'msg' not in self.data:
                    self.data['msg'] = m[1]
                    first_from = p
                    marked_edges[p] = True
                    for p in range(self.deg):
                        if not marked_edges[p]:
                            self.send(p, ('shout', self.data['msg']))
                else:
                    self.send(p, ('echo', self.data['msg']))
   
def run(n):
    msg = 'test'
    t = topo.random(n, n//2)
    net = Network(ShoutAndEcho, t)
    net.nodes[0].data['shout'] = msg
    net.run()
    
    # check that it worked
    for n in net.nodes:
        if n.data['msg'] != msg:
            n.log("did not get the message!")

if __name__ == '__main__':
    run(47)
