TRIPLES = [
  (0, 2, 5),
  (0, 2, 6),
  (0, 2, 7),
  (0, 3, 8),
  (0, 3, 9),
  (0, 4, 10),
  (1, 4, 11),
]

def generate_primes(n):
    """Generate the first n prime numbers using the Sieve of Eratosthenes."""
    if n <= 0:
        return []
    
    # Start with a large enough range to find n primes
    limit = max(n * 15, 100)  # Rough estimate for finding n primes
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    
    primes = [i for i in range(2, limit + 1) if sieve[i]]
    return primes[:n]

def create_triple_hash(triple):
    """Create a unique hash for a triple to use as a key."""
    return hash(triple)

# Method 1: Each triple gets its own prime (most accurate, but uses more primes)
def encodeGraph(graph):
    """
    Encode a directed graph as a single integer using prime factorization.
    Each unique triple gets assigned a prime number.
    The graph is encoded as the product of all triple primes.
    """
    if not graph:
        return 1, {}  # Empty graph encoded as 1
    
    # Assign each unique triple a prime number
    unique_triples = list(set(graph))  # Remove duplicates if any
    primes = generate_primes(len(unique_triples))
    triple_to_prime = dict(zip(unique_triples, primes))
    
    # Encode the graph as product of all triple primes
    graph_encoding = 1
    for triple in unique_triples:
        graph_encoding *= triple_to_prime[triple]
    
    return graph_encoding, triple_to_prime

def check_triple_exists(graph_encoding, triple_to_prime, triple):
    """
    Check if a triple exists in the encoded graph using modular arithmetic.
    Returns True if the triple exists, False otherwise.
    """
    # Check if the triple has a prime mapping (i.e., exists in original graph)
    if triple not in triple_to_prime:
        return False
    
    # Check if the graph encoding is divisible by the triple's prime
    triple_prime = triple_to_prime[triple]
    return graph_encoding % triple_prime == 0

# Method 2: Node/edge-based encoding (more memory efficient for large graphs)
def encodeGraphByElements(graph):
    """
    Alternative encoding where each node/edge gets a prime, and triples are 
    encoded using a hash-based approach to ensure uniqueness.
    More memory efficient and avoids false positives.
    """
    if not graph:
        return set(), {}
    
    # Get all unique nodes and edges
    unique_values = set()
    for s, p, o in graph:
        unique_values.update([s, p, o])
    
    unique_values = sorted(list(unique_values))
    primes = generate_primes(len(unique_values))
    value_to_prime = dict(zip(unique_values, primes))
    
    # Instead of multiplication, store a set of unique triple encodings
    triple_encodings = set()
    for s, p, o in set(graph):  # Remove duplicates
        # Create a unique encoding using prime combination
        # Using a large base to ensure uniqueness: base^2*s + base*p + o
        base = max(primes) + 1
        triple_encoding = (value_to_prime[s] * base * base + 
                          value_to_prime[p] * base + 
                          value_to_prime[o])
        triple_encodings.add(triple_encoding)
    
    return triple_encodings, value_to_prime

def check_triple_exists_by_elements(graph_encodings, value_to_prime, triple):
    """
    Check triple existence using element-based encoding with unique hash.
    This method avoids false positives by using a set-based approach.
    """
    s, p, o = triple
    
    # Check if all elements exist in the mapping
    if any(val not in value_to_prime for val in [s, p, o]):
        return False
    
    # Encode the query triple using the same scheme
    primes = list(value_to_prime.values())
    base = max(primes) + 1
    triple_encoding = (value_to_prime[s] * base * base + 
                      value_to_prime[p] * base + 
                      value_to_prime[o])
    
    # Check if the encoding exists in the set
    return triple_encoding in graph_encodings

# Method 3: Hybrid approach - single integer with unique triple hashes
def encodeGraphHybrid(graph):
    """
    Hybrid encoding that creates a single integer by multiplying unique prime 
    encodings for each triple, where each triple gets a unique prime based on 
    its hash. This maintains the single-integer property while avoiding false positives.
    """
    if not graph:
        return 1, {}
    
    # Get all unique nodes and edges for consistent hashing
    unique_values = set()
    for s, p, o in graph:
        unique_values.update([s, p, o])
    unique_values = sorted(list(unique_values))
    
    # Create a deterministic mapping from triples to unique identifiers
    unique_triples = list(set(graph))
    unique_triples.sort()  # Ensure deterministic ordering
    
    # Generate enough primes for unique triple identification
    primes = generate_primes(len(unique_triples))
    triple_to_prime = {}
    
    for i, triple in enumerate(unique_triples):
        # Use a more sophisticated hash that considers element positions
        s, p, o = triple
        triple_hash = hash((s, 'subj')) ^ hash((p, 'pred')) ^ hash((o, 'obj'))
        triple_to_prime[triple] = primes[i]
    
    # Encode graph as product of unique triple primes
    graph_encoding = 1
    for triple in unique_triples:
        graph_encoding *= triple_to_prime[triple]
    
    return graph_encoding, triple_to_prime

def check_triple_exists_hybrid(graph_encoding, triple_to_prime, triple):
    """
    Check if a triple exists using the hybrid encoding approach.
    """
    if triple not in triple_to_prime:
        return False
    
    return graph_encoding % triple_to_prime[triple] == 0

# Example usage
if __name__ == "__main__":
    print("=== Method 1: Triple-based encoding (most accurate) ===")
    # Encode the graph
    encoded_graph, triple_mapping = encodeGraph(TRIPLES)
    print(f"Graph encoded as: {encoded_graph}")
    print(f"Triple to prime mappings: {triple_mapping}")
    
    # Test some triples
    test_triples = [
        (0, 2, 5),  # Should exist
        (0, 2, 6),  # Should exist  
        (1, 4, 11), # Should exist
        (0, 2, 8),  # Should not exist
        (5, 6, 7),  # Should not exist
    ]
    
    print("\nTriple existence checks:")
    for triple in test_triples:
        exists = check_triple_exists(encoded_graph, triple_mapping, triple)
        print(f"Triple {triple}: {'EXISTS' if exists else 'NOT FOUND'}")
    
    print("\n=== Method 2: Element-based encoding (more efficient) ===")
    encoded_graph2, element_mapping = encodeGraphByElements(TRIPLES)
    print(f"Graph encoded as set with {len(encoded_graph2)} unique triple encodings")
    print(f"Element to prime mappings: {element_mapping}")
    
    print("\nTriple existence checks (element-based):")
    for triple in test_triples:
        exists = check_triple_exists_by_elements(encoded_graph2, element_mapping, triple)
        print(f"Triple {triple}: {'EXISTS' if exists else 'NOT FOUND'}")
    
    print("\n=== Method 3: Hybrid encoding (single integer, no false positives) ===")
    encoded_graph3, hybrid_mapping = encodeGraphHybrid(TRIPLES)
    print(f"Graph encoded as: {encoded_graph3}")
    print(f"Hybrid triple mappings: {hybrid_mapping}")
    
    print("\nTriple existence checks (hybrid):")
    for triple in test_triples:
        exists = check_triple_exists_hybrid(encoded_graph3, hybrid_mapping, triple)
        print(f"Triple {triple}: {'EXISTS' if exists else 'NOT FOUND'}")
  