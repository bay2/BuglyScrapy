FROM python:3.6.7-alpine3.8

RUN mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn && \
    mkdir -p /usr/src/code

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

ENV PROJECT manage

EXPOSE 5000

# CMD "/usr/local/bin/gunicorn -w 2 -b :5000 BuglyFlask:app"

CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":5000", "BuglyFlask:app"]