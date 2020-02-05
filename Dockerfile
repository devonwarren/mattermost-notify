
FROM alpine:latest

# input env variables
ENV MESSAGE_TEXT "Test Mattermost Notification"
ENV MATTERMOST_HOOK_URL "http://google.com"
ENV DEBUG "false"

# volume for importing json files
RUN mkdir /json-input
#VOLUME /json-input

RUN mkdir /templates

# install curl and python
RUN apk add curl python3 bash
RUN pip3 install --upgrade pip && pip3 install Jinja2 requests

# copy run script
COPY ./run.py .
COPY ./run.sh .

# testing
RUN echo '{"test":1,"test2":false}' > /json-input/test1.json
RUN echo '{"new_test":1}' > /json-input/test2.json
#RUN ls /json-input

# use 
ENTRYPOINT [ "bash", "run.sh" ]