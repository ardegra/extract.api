FROM python:3

ADD . /root/app
WORKDIR /root/app

ENV SENTRY_DSN="https://c66c868785814c9b8b00c2778f50f835:4faabc1a01634d3c86d6a359ca1508f7@sentry.io/286639"

RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn run:api -b 0.0.0.0:8000 --reload