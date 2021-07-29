# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update
RUN apt-get install -y libmagic1
RUN apt-get install -y openssh-client git && mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
COPY . .
RUN pip3 install git+https://git@github.com/jonathan-w-fiverr/resume_parser.git@master
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install python-magic
RUN pip install nltk
RUN pip install spacy==2.3.5
RUN pip install aiofiles
RUN pip install python-multipart
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz

RUN pip install pyresparser
RUN python3 -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader universal_tagset
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader brown
RUN python -m nltk.downloader maxent_ne_chunker

CMD [ "uvicorn", "--host", "0.0.0.0" , "main:app", "--reload"]