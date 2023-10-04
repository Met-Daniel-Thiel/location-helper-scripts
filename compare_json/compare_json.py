'''
Directions for use
1. copy the contents of two json files you would like to compare into json_file/j1.json and json_file/j1.json
2. run compare_json.py
3. review the differences in differences.json.
    - all differences are highlighted
    - "$delete" indicates a value present in j1 is missing from j2
    - "$insert" indicates a value that was not present in j1 is present in j2
'''

import os
import json
import jsondiff

# import and name the json files
json_path = "compare_json/json_files"
jsons = [json.load(open(json_path + "/" + j, 'r')) for j in os.listdir(json_path)]
j1 = jsons[0]
j2 = jsons[1]

# compare j1 and j2
diff = jsondiff.diff(j1, j2, syntax='symmetric')

# Convert keys to strings
def convert_keys_to_str(d):
    if isinstance(d, dict):
        return {str(k): convert_keys_to_str(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_keys_to_str(v) for v in d]
    else:
        return d
diff = convert_keys_to_str(diff)

# Save the formatted differences to a JSON file
with open("compare_json/differences.json", "w") as outfile:
    json.dump(diff, outfile, indent=2)