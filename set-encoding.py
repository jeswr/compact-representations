def encode_set(number_set, max_value):
    """
    Encode a set of numbers to a unique integer value.
    
    Args:
        number_set: A set or iterable of integers, each <= max_value
        max_value: The maximum value any number in the set can have
    
    Returns:
        A unique integer representing the set
    
    Raises:
        ValueError: If any number in the set is greater than max_value or negative
    """
    if not number_set:
        return 0
    
    # Validate input
    for num in number_set:
        if num < 0 or num > max_value:
            raise ValueError(f"Number {num} is out of range [0, {max_value}]")
    
    # Create binary representation where bit i is 1 if i is in the set
    encoded = 0
    for num in number_set:
        encoded |= (1 << num)  # Set bit at position 'num'
    
    return encoded


def decode_set(encoded_value, max_value):
    """
    Decode an integer back to the original set of numbers.
    
    Args:
        encoded_value: The integer value representing the encoded set
        max_value: The maximum value any number in the original set could have
    
    Returns:
        A set of integers representing the decoded set
    
    Raises:
        ValueError: If encoded_value is negative
    """
    if encoded_value < 0:
        raise ValueError("Encoded value must be non-negative")
    
    if encoded_value == 0:
        return set()
    
    decoded_set = set()
    
    # Check each bit position up to max_value
    for i in range(max_value + 1):
        if encoded_value & (1 << i):  # Check if bit i is set
            decoded_set.add(i)
    
    return decoded_set


# Example usage and test
if __name__ == "__main__":
    # Test with some example sets
    MAX = 10
    
    test_sets = [
        set(),           # Empty set
        {0},            # Single element
        {1, 3, 5},      # Multiple elements
        {0, 2, 4, 6, 8, 10},  # Even numbers
        {MAX},          # Maximum value
        set(range(MAX + 1))  # All possible values
    ]
    
    print("Testing set encoding and decoding:")
    print("-" * 40)
    
    for test_set in test_sets:
        encoded = encode_set(test_set, MAX)
        decoded = decode_set(encoded, MAX)
        
        print(f"Original set: {sorted(test_set) if test_set else 'empty'}")
        print(f"Encoded value: {encoded}")
        print(f"Decoded set: {sorted(decoded) if decoded else 'empty'}")
        print(f"Match: {test_set == decoded}")
        print()
    
    # Demonstrate uniqueness
    print("Demonstrating uniqueness:")
    print("-" * 25)
    encodings = {}
    for i in range(2**(MAX + 1)):  # All possible subsets
        test_set = set()
        for j in range(MAX + 1):
            if i & (1 << j):
                test_set.add(j)
        
        encoded = encode_set(test_set, MAX)
        if encoded in encodings:
            print(f"ERROR: Non-unique encoding found!")
        else:
            encodings[encoded] = test_set
    
    print(f"Successfully encoded {len(encodings)} unique sets with MAX={MAX}")
    print(f"Encoding range: 0 to {max(encodings.keys())}")
