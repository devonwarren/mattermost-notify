import json, os, fnmatch
from jinja2 import Environment, FileSystemLoader

json_data = {}
load_dir = "/json-input"
template_dir = "/templates"

# get list of files in json dir (first level only for now)
file_list = os.listdir(load_dir)
for file in file_list:
    # only grab .json files
    if fnmatch.fnmatch(file, "*.json"):
        with open(os.path.join(load_dir,file)) as json_file:
            # load json data into a variable using the filename as the key
            json_data[file[:-5]] = json.load(json_file)

print(json_data)


# setup jinja
tpl_loader = FileSystemLoader(template_dir)
env = Environment(loader=tpl_loader)

template = env.get_template('test.jinja')
output = template.render(json=json_data)
print(output)