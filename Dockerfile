FROM python:3.10
USER root
RUN mkdir /sensor-app
COPY . /sensor-app/
WORKDIR /sensor-app/
RUN pip3 install -r requirements.txt
EXPOSE 8000
SHELL [ "fuser", "-k", "8000/tcp" ] 
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]