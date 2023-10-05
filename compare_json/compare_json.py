'''
Directions for use
1. place two json files in compare_json/json_files. j1 and j2 can be over ridden or replaced. json file names are not important.
2. run compare_json.py
3. review the differences in differences.json.
    - all differences are highlighted
    - "$delete" indicates a value has been removed
    - "$insert" indicates a value has been added
'''

import os
import json
import jsondiff

# import and name the json files
json_path = "compare_json/json_files"
jsons = [json.load(open(json_path + "/" + j, 'r')) for j in os.listdir(json_path)]
j1 = jsons[0]
j2 = jsons[1]

# compare j1 and j2, ignoring order
diff = jsondiff.diff(j1, j2, syntax='symmetric')

# Convert keys to strings json does not accept ints
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