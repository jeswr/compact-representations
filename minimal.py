RANGES = 12
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

def has_patterns(graph, patterns):
  """Check if ALL of the given patterns exist in the graph."""
  # Check each pattern individually - all must match
  for pattern in patterns:
    s, p, o = pattern
    
    # Create a mask for this specific pattern
    mask = 0
    
    # Generate all possible triples that match this pattern
    s_values = [s] if s is not None else range(RANGES)
    p_values = [p] if p is not None else range(RANGES)
    o_values = [o] if o is not None else range(RANGES)
    
    # Set bits in mask for all matching positions for this pattern
    for s_val in s_values:
      for p_val in p_values:
        for o_val in o_values:
          mask |= (1 << encode_triple((s_val, p_val, o_val)))
    
    # If this pattern doesn't match, return False immediately
    if (graph & mask) == 0:
      return False
  
  # All patterns matched
  return True

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

# Test has_patterns with multiple patterns - ALL must match
patterns_all_match = [
  (0, None, 8),    # Should match (0, 3, 8)
  (0, 2, None),    # Should match (0, 2, 5), (0, 2, 6), (0, 2, 7)
]
print(has_patterns(graph, patterns_all_match))  # True - both patterns match

patterns_some_match = [
  (0, None, 8),    # Should match (0, 3, 8)
  (1, None, 8),    # No match
  (0, 2, None),    # Should match (0, 2, 5), (0, 2, 6), (0, 2, 7)
]
print(has_patterns(graph, patterns_some_match))  # False - not all patterns match

patterns_no_match = [
  (1, None, 8),    # No match
  (0, 1, None),    # No match
  (5, None, None), # No match
]
print(has_patterns(graph, patterns_no_match))  # False - no patterns match
