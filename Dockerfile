FROM python:3.10
USER root
RUN mkdir /sensor-app
COPY . /sensor-app/
WORKDIR /sensor-app/
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD [ "gunicorn","wsgi:app","--host","0.0.0.0","--port","8000" ]
