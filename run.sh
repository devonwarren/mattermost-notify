
# export message to jinja
echo ${MESSAGE_TEXT} > /app/templates/default.jinja;

# show json files for debugging
if [ $(echo $DEBUG | tr '[A-Z]' '[a-z]') == "true" ]; then
    echo "=== JSON FILES ===";
    ls /app/json-input;
    echo "=== END OF JSON LIST ==="
fi

# run preprocessor script
if [ "${PREPROCESS_PYTHON}" != "" ]; then
    echo "Running Preprocess script... "
    python3 ${PREPROCESS_PYTHON}
fi

# run that magic python script
python3 /app/run.py ${MATTERMOST_HOOK_URL}