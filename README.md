distributed-algorithms-emulator
===============================

An emulator of the model we use at the Distributed Algorithms class at my uni (so that I can try writing the actual code).

`da.py` contains the Node and Network classes used to implement the model. If you just want to use this, you don't want to read `da.py`.

See stuff in the `examples/` directory for usage examples and some of the 
algorithms taught in the class.

Currently implemented algorithms:

- [broadcast and convergecast on tree topology](https://github.com/AnotherKamila/distributed-algorithms-emulator/blob/master/examples/broadcast.py)

------------------------------------------------------------------------------

TODO:

- Currently this is implemented via threads, so there is no control over message scheduling. Add an explicit scheduler (perhaps switching to coroutines instead of threads). Perhaps in the far future allow for a sophisticated adversary?
- Currently only bidirectional edges are supported, because I am lazy  -- allow assymetric edges too.
  - This is easy to fix: just rewrite building of the local port -> node mapping.
- A visualization would be nice. Perhaps a webpage with a client-side python interpreter, wired to D3? :D
  - Maybe also add an interactive message scheduler :D
