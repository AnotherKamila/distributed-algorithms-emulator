"""Utilities for creating and manipulating network topologies."""

from random import sample, shuffle

def procedural(it, f):
    """Procedural topology.

    - it: iterator of node labels
    - f: label -> [label] -- defines the edges
    """
    return { i: f(i) for i in it }

def randomized(t):
    for ps in t.values(): shuffle(ps)
    return t

def bidirectional(t):
    for i in t:
        for j in t[i]:
            if not i in t[j]:
                t[j].append(i)
    return t

def with_self(t):
    return { i: [i]+t[i] for i in t }

def without_self(t):
    return { i: [ n for n in t[i] if n != i ] for i in t }

def K_SOD(n):
    return procedural(range(n), lambda i: [(i+d)%n for d in range(1, n)])

def C_SOD(n):
    return procedural(range(n), lambda i: [(i-1)%n, (i+1)%n])

def K(n):
    return randomized(K_SOD(n))

def C(n):
    return randomized(C_SOD(n))

def random(n, mind):
    """Does not guarantee that it's connected (TODO)!"""
    return bidirectional({i: sample(range(n), mind) for i in range(n)})
