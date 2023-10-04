import os
import json

json_path = "compare_json/json_files"
jsons = [json.load(open(json_path + "/" + j, 'r')) for j in os.listdir(json_path)]

j1 = jsons[1]

'''
def paths(j):
   if value = string
       return "key:value"
   else:
       return "key" + ":" + paths()
'''

def paths(j,s):
    for k in j:
        print(k)
        print(j[k])
        print()

        if isinstance(j[k], str):
            return k + ":" + j[k]
        else:
            return paths(j[k],s.append(k))



paths(j1,[])








