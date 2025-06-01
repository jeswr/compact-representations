# compact-representations

Compact representations for signing (shower thoughts that are likely premature optimisation for the most part)

---

Say we have a graph with 2 different nodes that are subjects, 14 are relations 16 are objects. We can then use the following triple based presentation

There are 10 * 5 * 7 possible edges that could exist in the graph and so 2^(2 * 14 * 16) = 2^448 possible graphs given those constraints.


Future:

* Alphanumeric encoding of this value (CBOR likely already handles some of this if we are going for that encoding).


References:

* https://stackoverflow.com/questions/37806678/encoding-directed-graph-as-numbers
