class TripleEncoder:
    """
    Encodes triples (a, b, c) to unique numeric values and vice versa.
    
    Each position has a known maximum value, and minimum is always 0.
    Uses a multi-base encoding scheme to ensure bijective mapping.
    """
    
    def __init__(self, max_values):
        """
        Initialize the encoder with maximum values for each position.
        
        Args:
            max_values: tuple/list of 3 integers representing max values for each position
                       e.g., (10, 5, 15) means position 0 can be 0-10, position 1 can be 0-5, etc.
        """
        if len(max_values) != 3:
            raise ValueError("Must provide exactly 3 maximum values")
        
        self.max_values = tuple(max_values)
        self.ranges = tuple(max_val + 1 for max_val in max_values)  # +1 because we include 0
        
    def encode(self, triple):
        """
        Encode a triple (a, b, c) to a unique numeric value.
        
        Args:
            triple: tuple/list of 3 integers
            
        Returns:
            int: unique encoded value
        """
        if len(triple) != 3:
            raise ValueError("Must provide exactly 3 values")
        
        a, b, c = triple
        
        # Validate ranges
        if not (0 <= a <= self.max_values[0]):
            raise ValueError(f"First value {a} must be between 0 and {self.max_values[0]}")
        if not (0 <= b <= self.max_values[1]):
            raise ValueError(f"Second value {b} must be between 0 and {self.max_values[1]}")
        if not (0 <= c <= self.max_values[2]):
            raise ValueError(f"Third value {c} must be between 0 and {self.max_values[2]}")
        
        # Multi-base encoding: a * range1 * range2 + b * range2 + c
        encoded = a * self.ranges[1] * self.ranges[2] + b * self.ranges[2] + c
        return encoded
    
    def decode(self, encoded_value):
        """
        Decode a numeric value back to the original triple.
        
        Args:
            encoded_value: int to decode
            
        Returns:
            tuple: original triple (a, b, c)
        """
        if encoded_value < 0:
            raise ValueError("Encoded value must be non-negative")
        
        # Reverse the encoding process
        c = encoded_value % self.ranges[2]
        remaining = encoded_value // self.ranges[2]
        
        b = remaining % self.ranges[1]
        a = remaining // self.ranges[1]
        
        # Validate the decoded values are within bounds
        if a > self.max_values[0] or b > self.max_values[1] or c > self.max_values[2]:
            raise ValueError(f"Invalid encoded value {encoded_value}")
        
        return (a, b, c)
    
    def get_max_encoded_value(self):
        """Get the maximum possible encoded value."""
        return self.ranges[0] * self.ranges[1] * self.ranges[2] - 1
    
    def get_encoded_value_range(self):
        """
        Get the complete range of possible encoded values.
        
        Returns:
            tuple: (min_value, max_value) where min_value is always 0
        """
        min_value = 0  # Always 0 when all triple values are at minimum (0, 0, 0)
        max_value = self.get_max_encoded_value()
        return (min_value, max_value)
    
    def get_total_possible_encodings(self):
        """
        Get the total number of possible unique encodings.
        
        Returns:
            int: total number of unique triples that can be encoded
        """
        return self.ranges[0] * self.ranges[1] * self.ranges[2]
    
    def get_encoding_info(self):
        """
        Get comprehensive information about the encoding space.
        
        Returns:
            dict: information about the encoding including ranges, totals, etc.
        """
        min_val, max_val = self.get_encoded_value_range()
        total_encodings = self.get_total_possible_encodings()
        
        return {
            'max_triple_values': self.max_values,
            'value_ranges': self.ranges,
            'encoded_value_range': (min_val, max_val),
            'total_possible_encodings': total_encodings,
            'encoding_efficiency': f"{total_encodings} unique values using {max_val + 1} integers"
        }


def example_usage():
    """Demonstrate usage with some examples."""
    # Example: max values are (10, 5, 15)
    # This means position 0 can be 0-10, position 1 can be 0-5, position 2 can be 0-15
    encoder = TripleEncoder([10, 5, 15])
    
    # Test with the example triple (3, 2, 9)
    test_triple = (3, 2, 9)
    encoded = encoder.encode(test_triple)
    decoded = encoder.decode(encoded)
    
    print(f"Original triple: {test_triple}")
    print(f"Encoded value: {encoded}")
    print(f"Decoded triple: {decoded}")
    print(f"Encoding successful: {test_triple == decoded}")
    print()
    
    # Test a few more examples
    test_cases = [(0, 0, 0), (10, 5, 15), (5, 3, 7), (1, 1, 1)]
    
    print("More test cases:")
    for triple in test_cases:
        encoded = encoder.encode(triple)
        decoded = encoder.decode(encoded)
        print(f"{triple} -> {encoded} -> {decoded} ✓")
    
    print(f"\nMaximum encoded value: {encoder.get_max_encoded_value()}")
    print(f"Total possible unique triples: {encoder.get_total_possible_encodings()}")
    
    # Show the complete range information
    min_val, max_val = encoder.get_encoded_value_range()
    print(f"Encoded value range: {min_val} to {max_val}")
    
    # Show comprehensive encoding information
    print("\nEncoding Information:")
    info = encoder.get_encoding_info()
    for key, value in info.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    example_usage()
