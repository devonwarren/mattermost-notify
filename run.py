import json, os, fnmatch, requests, sys
from jinja2 import Environment, FileSystemLoader

json_data = {}
load_dir = "/json-input"
template_dir = "/templates"

# parse cli args
#parser = argparse.ArgumentParser()
#parser.add_argument('--webhook', nargs=1, help="URL to post data to")
#parser.add_argument('--message', nargs=1, help="URL to post data to")
#args = parser.parse_args()
print(sys.argv)

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

template = env.get_template('default.jinja')
output = template.render(data=json_data)
print(output)


# push request into mattermost
r = requests.post(sys.argv[1], data = {'text':output}, verify=False)
print(r.text)

r.raise_for_status()