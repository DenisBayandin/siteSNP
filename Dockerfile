FROM python:3.11
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./sitevotephoto ./sitevotephoto

CMD [ "python", "./sitevotephoto/manage.py", "runserver", "127.0.0.1:8000"]