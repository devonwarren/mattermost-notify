
echo ${MESSAGE_TEXT} > /templates/default.jinja

python3 run.py ${MATTERMOST_HOOK_URL}