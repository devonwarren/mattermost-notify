# mattermost-notify
**A template based Mattermost (or Slack) notification docker image for use in CI steps**
This project was created so our company could load in json files as needed and parse them using Jinja2 and then dump output into Mattermost using Gitlab CI. For example if you have a code scanning tool you can extract a json result from, simply put that file into **/json-input** and it will be available to display as you wish into mattermost


## Variables
These variables can be set when running the docker image to customize the functionality
| Variable | Default | Description |
| --- | --- | --- |
| MESSAGE_TEXT | Test Mattermost Notification | A value that will be sent to Mattermost after rendering through Jinja |
| MATTERMOST_HOOK_URL | https://google.com | The full url that the HTTP POST request will go to (usually requires the incoming hook token in it) |
| DEBUG | False | If set to True will enable additional output including a dump of all the variables run against Jinja |
| TEMPLATE_FILE | default.jinja | A file inside /templates that will rendered against to post the message. If Using MESSAGE_TEXT this will dump into the default.jinja file automatically |
| CHANNEL |  | The channel to put notification into. If not set will use the default set up for incoming hook |