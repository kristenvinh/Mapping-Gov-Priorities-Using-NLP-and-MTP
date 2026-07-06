import json
import glob

# 1. Find all files matching your timestamped naming pattern
# If they are in a specific folder, update the path like: 'data_folder/extracted_initiatives_*.json'
file_pattern = 'extracted_initiatives_*.json'
json_files = glob.glob(file_pattern)

master_list = []

# 2. Loop through each file and add its contents to the master list
for file_path in json_files:
    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Using .extend() because 'data' is a list, and we want to add its items, not the list itself
        master_list.extend(data)

# 3. Export the combined data into a single master file
output_file = 'ALL_extracted_initiatives_merged.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(master_list, f, indent=4)

print(f"\nSuccess! Merged {len(json_files)} files into {output_file}.")
print(f"Total policy initiatives extracted: {len(master_list)}")