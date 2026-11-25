
import threading

def count():
    for i in range(1, 6):
        print("Count:", i)

def square():
    for i in range(1, 6):
        print("Square:", i*i)

def cube():
    for i in range(1, 6):
        print("Cube:", i*i*i)

# Create threads
t1 = threading.Thread(target=count)
t2 = threading.Thread(target=square)
t3 = threading.Thread(target=cube)

# Start threads
t1.start()
t2.start()
t3.start()

# Wait for completion
t1.join()
t2.join()
t3.join()

print("All tasks completed!")
