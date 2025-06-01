RANGES = 10
SET_RANGES = RANGES ** 3 - 1

def encode_objects(objects):
  encoded = 0
  for o in objects:
    encoded |= (1 << o)
  return encoded

def encode_predicates(predicates):
  encoded = 0
  for p, objects in predicates.items():
    encoded |= (1 << p * RANGES + encode_objects(objects))
  return encoded

def encode_triples(triples):
  encoded = 0
  for s, predicates in triples.items():
    encoded |= (1 << s * RANGES * RANGES + encode_predicates(predicates))
  return encoded

TRIPLES = {
  0: {
    2: [5, 6, 7],
    3: [8, 9],
  },
  1: {
    2: [5, 6, 7],
    3: [8, 9],
  },
}

print(encode_triples(TRIPLES))

# for s, predicates in TRIPLES.items():
#   print(s)
#   for p, objects in predicates.items():
#     print(encode_predicates(p))
#     print(encode_objects(objects))
