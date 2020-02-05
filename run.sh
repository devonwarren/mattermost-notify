
# export message to jinja
echo ${MESSAGE_TEXT} > /templates/default.jinja;

# show json files for debugging
if [ "${DEBUG,,}" == "true" ]; then
    echo "=== JSON FILES ===";
    ls /json-input;
    echo "=== END OF JSON LIST ==="
fi

# run that magic python script
python3 /run.py ${MATTERMOST_HOOK_URL}