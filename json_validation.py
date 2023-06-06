import sys
import json

if len(sys.argv) != 2:
    print("Usage: python3 json_validation.py <filename>")
    exit(1)

filename = sys.argv[1]
try:
    with open(filename, "r") as f:
        data = json.load(f)
    print("JSON is valid")
    if isinstance(data, list):
        print("List length: " + str(len(data)))
    elif isinstance(data, dict):
        print("Dict length: " + str(len(data)))
    else:
        print("Unknown type")
except ValueError as e:
    print("Error: " + str(e))
    exit(1)
