
FROM alpine:3.12

# input env variables
ENV MESSAGE_TEXT "Test Mattermost Notification"
ENV MATTERMOST_HOOK_URL "http://google.com"
ENV DEBUG "false"
ENV TEMPLATE_FILE "default.jinja"
ENV CARD_TEMPLATE_FILE ""
ENV CHANNEL ""
ENV USERNAME ""
ENV ICON_URL ""
ENV ICON_EMOJI ""
ENV PREPROCESS_PYTHON ""

# create user so not running as root
RUN adduser -D notifyuser

# directory for importing json files and templates
RUN mkdir /app
RUN chown -R notifyuser /app && chmod 775 /app

# install curl and python and other potential tools
RUN apk add curl git python3 bash py3-numpy py3-pip
RUN pip3 install --upgrade pip && pip3 install Jinja2 requests

# copy run script
COPY --chown=notifyuser ./run.py /app
COPY --chown=notifyuser ./run.sh /app

# start running as non-root
USER notifyuser

# create directories for importing json files and templates
RUN mkdir /app/json-input && mkdir /app/templates

# use bash startup script
ENTRYPOINT [ "sh", "/app/run.sh" ]