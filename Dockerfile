FROM python:3

ADD . /root/app
WORKDIR /root/app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn run:api -b 0.0.0.0:8000 --reload