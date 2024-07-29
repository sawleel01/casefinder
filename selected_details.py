import json

with open('details.json', 'r') as f:
    data = json.load(f)

print("Data loaded from JSON:", json.dumps(data, indent=4))


selected_data = {
    '1': data.get('1'),
    '3': data.get('3'),
    '4': data.get('4')
}

with open('final.json', 'w') as f:
    json.dump(selected_data, f, indent=4)

print("Selected details have been written to final.json")
