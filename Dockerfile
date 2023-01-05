FROM python:3.10
RUN mkdir /sensor-app
COPY . /sensor-app/
WORKDIR /sensor-app/
RUN pip3 install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --worker=1 --bind 0.0.0.0:$PORT app:app