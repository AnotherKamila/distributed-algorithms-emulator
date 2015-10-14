"""Tests if it "compiles" (except that it doesn't).

Also: trivial usage example.
"""

from da import Node, Network
from dautils import procedural_topo

class MyNode(Node):
    def run(self):
        self.send(0, self.ID)
        p, m = self.recv()
        self.log("received message {} on port {}", m, p)

def run(n):
    topo = procedural_topo(range(n), lambda i: [ (i+d)%n for d in range(1, n) ])
    net = Network(MyNode, topo)
    net.run()

if __name__ == '__main__':
    run(47)
