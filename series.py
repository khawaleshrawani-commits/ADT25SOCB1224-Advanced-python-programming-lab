
import pandas as pd
import numpy as np

# Create Series of 10 random numbers
s = pd.Series(np.random.randint(1, 100, 10))

print("Original Series:")
print(s)

# Indexing
print("\nElement at index 2:", s[2])

# Filtering
print("\nNumbers greater than 50:")
print(s[s > 50])

# Statistical operations
print("\nMean:", s.mean())
print("Median:", s.median())
print("Minimum:", s.min())
print("Maximum:", s.max())
