FROM alpine:3.7

RUN apk add python3


WORKDIR /usr/src/scraper

COPY scraper.py ./
COPY server.py ./
COPY database.py ./
COPY requirements.txt ./
COPY cert.pem ./
COPY key_unenc.pem ./

RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "./server.py"]
