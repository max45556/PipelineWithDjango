FROM python:3.9-buster
LABEL maintener='maxapp.com'
#RUN apk --no-cache add musl-dev linux-headers g++

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY . /app

RUN python -m venv /py && \
  pip install --upgrade pip && \
  pip install tensorflow && \
  pip install black && \
  pip install flake8 && \
  pip install mypy && \
  pip install pyflakes && \
  pip install pylint && \
  pip install -r /requirements.txt && \
  pip install typing-extensions --upgrade && \
  pip install setuptools wheel

RUN adduser --disabled-password --no-create-home app

USER root
WORKDIR /app
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000

# docker run --name django -d --network jenkins_bridge django