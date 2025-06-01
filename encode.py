# Encode arbitrary sized integers as UTF-8 strings for compression
# This is the range of valid UTF-8 characters: https://docs.python.org/3/library/functions.html#chr
import sys
C = 1_114_111

def encode(n): 
  if not n: return "0"
  return encode(n//C).lstrip("0") + chr(n%C)

def decode(s):
  if not s: return 0
  return decode(s[:-1]) * C + ord(s[-1])

sys.setrecursionlimit(30 ** 3)
print(encode(2 ** (27 ** 3)))
