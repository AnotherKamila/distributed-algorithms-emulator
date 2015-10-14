import time
import random
from queue import Queue
from threading import Thread
#from internal import NodeWorker

class Node:
    """Implements the node concept.

    Node cannot be used directly -- you need to subclass it and implement the
    algorithm in a `run(self)` method. See examples.

    Note: it is an error to call any methods (except __init__) when this node is
    not part of a network (i.e. when self._network_ref is None).
    """

    def __init__(self, ID, network_ref=None):
        self.ID, self._network_ref, self.nports = ID, network_ref, 0
        self.data = {}

    def send(self, port, m):
        """Sends a message through the given port. Non-blocking."""
        self._network_ref.send(self._label, port, m)

    def recv(self):
        """Receives a message from any port. Blocking."""
        return self._network_ref.recv(self._label)

    def peek(self):
        """Peeks at the first incoming message (not removing it). Blocking."""
        return self._network_ref.peek(self._label)

    def log(self, s, *args):
        """Log to stdout, adding node ID and timestamp."""
        t = time.time() - self._network_ref._start_time
        print(("[{:10}/{:6} {: 3.6f}] " + s).format(self._label, self.ID, t, *args))

class NodeThread(Thread):
    def __init__(self, node, termQ):
        Thread.__init__(self)
        self.node = node
        self.termQ = termQ

    def run(self):
        self.termQ.put(True)
        self.node.run()
        self.termQ.get(); self.termQ.task_done()

class Network:
    """TODO doc"""

    def __init__(self, nodecls, topo):
        self.net, self.msgs, self.nodes = {}, {}, []

        ids = random.sample(range(1000000), len(topo))
        for node_id, label, ports in zip(ids, topo.keys(), topo.values()):
            self.msgs[label] = Queue()
            n = nodecls(node_id, self)
            self.nodes.append(n)
            n.nports, n._label = len(ports), label
            for i, to in enumerate(ports):
                js = [ j for j, n in enumerate(topo[to]) if n == label ]
                assert len(js) == 1, "Topology is invalid!"
                self.net[(label, i)] = (to, js[0])

    def send(self, from_label, from_port, m):
        to_label, to_port = self.net[(from_label, from_port)]
        self.msgs[to_label].put((to_port, m))

    def recv(self, to_label):
        m = self.msgs[to_label].get()
        self.msgs[to_label].task_done()
        return m

    def peek(self, to_label):
        m = self.msgs[to_label].get()
        self.msgs[to_label].put(m)  # emulate not removing by re-adding
        return m

    def run(self):
        self._start_time = time.time()
        termQ = Queue()  # will be used as sync mechanism: pop on termination
        for n in self.nodes:
            thr = NodeThread(n, termQ)
            thr.daemon = True
            thr.start()
        termQ.join()  # wait for termination of all nodes
