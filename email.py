
import re

# Read text file
with open("sample.txt", "r") as file:
    text = file.read()

# Email pattern
pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Find valid email addresses
emails = re.findall(pattern, text)

print("Valid Email Addresses:")
for email in emails:
    print(email)
