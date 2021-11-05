FROM tiangolo/uwsgi-nginx:python3.7

COPY ./requirements.txt /

RUN pip3 install -r /requirements.txt

WORKDIR /application