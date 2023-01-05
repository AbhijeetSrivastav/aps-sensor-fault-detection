FROM python:3.10
RUN mkdir /sensor-app
COPY . /sensor-app/
WORKDIR /sensor-app/
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]