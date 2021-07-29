# syntax=docker/dockerfile:1
FROM python:3.6-slim-buster
WORKDIR /cv-srv
RUN apt-get update
RUN apt-get install -y libmagic1
RUN apt-get install -y openssh-client git && mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY ./requirements.txt /cv-srv/requirements.txt
COPY . /cv-srv

RUN pip install -r requirements.txt

WORKDIR app
RUN ls -lA
RUN ls -lA in/

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
