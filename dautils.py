def procedural_topo(it, f):
    return { i: f(i) for i in it }
