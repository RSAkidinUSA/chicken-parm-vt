FROM alpine:3.7

RUN apk add python3
RUN python3 -m pip install requests schedule beautifulsoup4

WORKDIR /usr/src/scraper

COPY scraper.py ./
COPY slack.env ./

CMD [ "python3", "./scraper.py"]
