import json, os, fnmatch, requests, sys, logging
from jinja2 import Environment, FileSystemLoader

load_dir = "/json-input"
template_dir = "/templates"

# allow debugging if enabled
if os.environ['DEBUG'].lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)

# parsed python args for debugging
logging.debug('System Arguments: ' + str(sys.argv))

# get list of files in json dir (first level only for now)
file_list = os.listdir(load_dir)
json_data = {}
for file in file_list:
    # only grab .json files
    if fnmatch.fnmatch(file, "*.json"):
        with open(os.path.join(load_dir,file)) as json_file:
            # load json data into a variable using the filename as the key (without extension)
            json_data[file[:-5]] = json.load(json_file)

logging.debug('JSON data (template tag- data): ' + str(json_data))
logging.debug('Environment vars (template tag- env): ' + str(os.environ))

# setup jinja
tpl_loader = FileSystemLoader(template_dir)
env = Environment(loader=tpl_loader)

# render template
template = env.get_template(os.environ['TEMPLATE_FILE'])
logging.debug('Using template file /templates/{0}'.format(os.environ['TEMPLATE_FILE']))
output = template.render(data=json_data, env=os.environ)
logging.debug('Template Output: ' + output)


# setup web request payload
payload = {}
extraOptions = [ 'CHANNEL', 'USERNAME', 'ICON_URL', 'ICON_EMOJI' ]

# iterate over additional options
for opt in extraOptions:
    if os.environ[opt]:
        payload[opt.lower()] = os.environ[opt]

payload['text'] = output

# push request into mattermost
r = requests.post(sys.argv[1], data=json.dumps(payload), verify=False, headers={'Content-Type': 'application/json'})
logging.debug('Request Body: ' + str(r.request.body))

# exit based on web response
r.raise_for_status()