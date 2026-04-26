import json
import sys

config_path = r"C:\Users\User\.openclaw\openclaw.json"

# Read the config
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Numbers to add to main WhatsApp allowFrom
numbers_to_add = [
    "+233244699428",
    "+233246466289", 
    "+233247582932",
    "+233538331872",
    "+233547676995",
    "+233558457027",
    "+31684021528"
]

# Get current allowFrom list
current_allow_from = config.get("channels", {}).get("whatsapp", {}).get("allowFrom", [])

# Add missing numbers
for number in numbers_to_add:
    if number not in current_allow_from:
        current_allow_from.append(number)

# Update the config
if "channels" not in config:
    config["channels"] = {}
if "whatsapp" not in config["channels"]:
    config["channels"]["whatsapp"] = {}
    
config["channels"]["whatsapp"]["allowFrom"] = current_allow_from

# Write back
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print(f"Updated WhatsApp allowFrom with {len(numbers_to_add)} numbers")
print(f"Total numbers now: {len(current_allow_from)}")
