FROM python:3.10
USER root
RUN mkdir /sensor-app
COPY . /sensor-app/
WORKDIR /sensor-app/
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT wsgi:app