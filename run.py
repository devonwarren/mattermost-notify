import json, os, fnmatch, requests, sys, logging
from jinja2 import Environment, FileSystemLoader
from pprint import pformat

load_dir = "/app/json-input"
template_dir = "/app/templates"

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

logging.debug(' JSON DATA (template tag- data): ')
logging.debug(pformat(json_data, indent=2, width=60) + '\n')
logging.debug(' ENVIRONMENT VARS (template tag- env): ')
logging.debug(str(os.environ) + '\n')

# setup jinja
tpl_loader = FileSystemLoader(template_dir)
env = Environment(loader=tpl_loader)

# render template
template = env.get_template(os.environ['TEMPLATE_FILE'])
logging.debug('Using template file /app/templates/{0}'.format(os.environ['TEMPLATE_FILE']))
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

# render card info if specified
if os.environ['CARD_TEMPLATE_FILE']:
    template = env.get_template(os.environ['CARD_TEMPLATE_FILE'])
    logging.debug('Using card template file /app/templates/{0}'.format(os.environ['CARD_TEMPLATE_FILE']))
    payload['props'] = {'card': template.render(data=json_data, env=os.environ)}
    logging.debug('Card Template Output: ' + payload['props']['card'])
    
# push request into mattermost
r = requests.post(sys.argv[1], data=json.dumps(payload), verify=False, headers={'Content-Type': 'application/json'})
logging.debug('Request Body: ' + str(r.request.body))

# exit based on web response
r.raise_for_status()