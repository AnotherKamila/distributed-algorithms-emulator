"""Tests if it "compiles" (except that it doesn't).

Also: trivial usage example.
"""

from da import Node, Network
from dautils import topo

class MyNode(Node):
    def run(self):
        self.send(0, self.ID)
        self.send(1, self.ID)
        p, m = self.recv(); self.log("received message {} on port {}", m, p)
        p, m = self.recv(); self.log("received message {} on port {}", m, p)

def run(n):
    net = Network(MyNode, topo.C(n))
    net.run()

if __name__ == '__main__':
    run(47)
