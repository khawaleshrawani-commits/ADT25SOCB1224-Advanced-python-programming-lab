
import gc
import time

# Check garbage collection status
print("Garbage Collection Enabled:", gc.isenabled())

# Create objects
a = []
b = []
a.append(b)
b.append(a)

# Delete references
del a
del b

# Check garbage before collection
print("Garbage before collection:", len(gc.garbage))

# Measure collection time
start = time.time()

# Manual garbage collection
collected = gc.collect()

end = time.time()

print("Objects Collected:", collected)
print("Garbage after collection:", len(gc.garbage))
print("Time Taken:", end - start)

print("Garbage Collection Completed")
