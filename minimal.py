RANGES = 10
SET_RANGES = RANGES ** 3 - 1

def encode_triple(triple):
  s, p, o = triple
  return s + p * RANGES + o * RANGES ** 2

def encode_graph(triples):
   # Create binary representation where bit i is 1 if i is in the set
  encoded = 0
  for triple in triples:
    encoded |= (1 << encode_triple(triple))  # Set bit at position 'num'
    
  return encoded

def has_triple(graph, triple):
  return graph & (1 << encode_triple(triple)) != 0

def has_pattern(graph, pattern):
  s, p, o = pattern
    # Create a mask with 1s at all positions that match the pattern
  mask = 0
  
  # Generate all possible triples that match the pattern
  s_values = [s] if s is not None else range(RANGES)
  p_values = [p] if p is not None else range(RANGES)
  o_values = [o] if o is not None else range(RANGES)
  
  # Set bits in mask for all matching positions
  for s_val in s_values:
    for p_val in p_values:
      for o_val in o_values:
        mask |= (1 << encode_triple((s_val, p_val, o_val)))

  # Check if any matching position has a bit set in the graph
  return (graph & mask) != 0

def has_any_patterns(graph, patterns):
  """Check if any of the given patterns exist in the graph using a single mask."""
  # Create a combined mask with 1s at all positions that match any pattern
  combined_mask = 0
  
  for pattern in patterns:
    s, p, o = pattern
    
    # Generate all possible triples that match this pattern
    s_values = [s] if s is not None else range(RANGES)
    p_values = [p] if p is not None else range(RANGES)
    o_values = [o] if o is not None else range(RANGES)
    
    # Set bits in combined_mask for all matching positions
    for s_val in s_values:
      for p_val in p_values:
        for o_val in o_values:
          combined_mask |= (1 << encode_triple((s_val, p_val, o_val)))
  
  # Check if any matching position has a bit set in the graph
  return (graph & combined_mask) != 0

TRIPLES = [
  (0, 2, 5),
  (0, 2, 6),
  (0, 2, 7),
  (0, 3, 8),
  (0, 3, 9),
]

graph = encode_graph(TRIPLES)
for triple in TRIPLES:
  print(has_triple(graph, triple)) # True

print(has_triple(graph, (0, 2, 8))) # False
print(has_pattern(graph, (0, None, 8))) # True
print(has_pattern(graph, (1, None, 8))) # False
print(has_any_patterns(graph, [(0, None, 8), (1, None, 8)])) # True
print(has_any_patterns(graph, [(1, None, 8), (1, None, 9)])) # False

print(graph)

C = 1_114_111

def encode(n): 
  if not n: return "0"
  return encode(n//C).lstrip("0") + chr(n%C)

print(encode(graph))
