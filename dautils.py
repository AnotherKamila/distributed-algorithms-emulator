import random

def randomize_ports(t):
    for ps in t.values(): random.shuffle(ps)
    return t

class topo:
    func = lambda it, f: { i: f(i) for i in it }
    randomized = lambda t: randomize_ports(t.copy())
    K_SOD = lambda n: topo.func(range(n), lambda i: [(i+d)%n for d in range(1, n)])
    K = lambda n: topo.randomized(topo.K_SOD(n))
    C_SOD = lambda n: topo.func(range(n), lambda i: [(i-1)%n, (i+1)%n])
    C = lambda n: topo.randomized(topo.C_SOD(n))
