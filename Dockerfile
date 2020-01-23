
FROM alpine:latest

# volume for importing json files
RUN mkdir /json-input
#VOLUME /json-input

RUN mkdir /templates

# install curl for later
RUN apk add curl python3
RUN pip3 install Jinja2

# testing
RUN echo '{"test":1,"test2":false}' > /json-input/test1.json
RUN echo '{"new_test":1}' > /json-input/test2.json
RUN ls /json-input
RUN echo 'test: {{ json.test2.new_test }}' > /templates/test.jinja


COPY ./run.py .


#ENTRYPOINT [ "ls", "/json-input" ]
ENTRYPOINT [ "python3", "run.py" ]