
# Read input file
with open("input.txt", "r") as file:
    lines = file.readlines()

# Count total lines
print("Total number of lines:", len(lines))

# Extract first two lines
data = lines[:2]

# Write into new file
with open("output.txt", "w") as file:
    file.writelines(data)

print("First two lines copied successfully!")
