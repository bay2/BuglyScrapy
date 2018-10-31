FROM joyzoursky/python-chromedriver:3.6-xvfb-selenium

COPY ./scrapyd.conf /etc/scrapyd/

EXPOSE 6800

RUN mkdir /code

COPY ./requirements.txt /code
WORKDIR /code

RUN pip3 install -r requirements.txt

CMD scrapyd