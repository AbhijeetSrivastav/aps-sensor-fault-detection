FROM python:3.10
USER root
RUN mkdir /sensor-app
COPY . /sensor-app/
WORKDIR /sensor-app/
RUN pip3 install -r requirements.txt
CMD gunicorn --workers=4 wsgi:app
