
import csv
import json

# Read CSV file
with open("input.csv", "r") as file:
    data = list(csv.DictReader(file))

# Convert CSV data into JSON
with open("output.json", "w") as file:
    json.dump(data, file, indent=4)

print("CSV file converted into JSON successfully!")
