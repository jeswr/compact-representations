# compact-representations

Compact representations for signing (shower thoughts that are likely premature optimisation for the most part)

---

It is possible to represent an entire graph as an integer. For instance we can do the following. 

```
RANGES = 12
SET_RANGES = RANGES ** 3 - 1

def encode_graph(triples):
   # Create binary representation where bit i is 1 if i is in the set
  encoded = 0
  for s, p, o in triples:
    encoded |= (1 << (s + p * RANGES + o * RANGES ** 2))  # Set bit at position 'num'
  
  return encoded

print(encode_graph([
  (0, 2, 5),
  (0, 2, 6),
  (0, 2, 7),
  (0, 3, 8),
  (0, 3, 9),
  (0, 4, 10),
  (1, 4, 11),
]))

// 381929249340500909518673926763019762113122063917922999147193572988224613193858636347368824440315729894269011655449184206466917222667305063276702809456926264585188589886938850162121178270409148086600312013604911089539626531473689532902477513279323740536728401227413098662566723111807316619568926342801121595240993844489054534304543672119482675096813174903607431974471380825928300171479110496490692678140113141079553830172803761664365766669841955361078534772944535177957570495238678628184096768
```

This also means that it is possible to prove that certain triples exist in the graph by proving that the signed integer satisfies particular numeric properties.

---

Future:

* Alphanumeric encoding of this value (CBOR likely already handles some of this if we are going for that encoding).

References:

* https://stackoverflow.com/questions/37806678/encoding-directed-graph-as-numbers
