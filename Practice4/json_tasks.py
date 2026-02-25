import json

# 1. Read JSON file
with open("/Users/zaniasahmardanovna/git/work/PP2/Practice4/sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':5}")
print("-" * 80)

# Navigate JSON structure (depends on your file structure)
interfaces = data["imdata"]

for item in interfaces:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")

    print(f"{dn:50} {descr:20} {speed:7} {mtu:5}")


# 2. Convert Python to JSON example
python_dict = {
    "name": "John",
    "age": 25,
    "city": "Almaty"
}

json_data = json.dumps(python_dict, indent=4)

with open("output.json", "w") as outfile:
    outfile.write(json_data)

print("\nJSON file created successfully.")