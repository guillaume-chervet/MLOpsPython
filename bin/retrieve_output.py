import json
import sys

args = sys.argv
filename = args[1]
json_property_name = args[2]
def get_last_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        return last_line.strip()

def json_to_dict(json_string):
    dict_obj = json.loads(json_string)
    return dict_obj


last_line = get_last_line(filename)
print("last_line")
print(last_line)
dict_obj = json_to_dict(last_line)


print(dict_obj[json_property_name])