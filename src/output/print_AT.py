import json

filename="02_AT_result.json"

with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

at_list = []
for item in data:
    at_list.extend(item.get("AT", []))

print(at_list)