FROM python:3.10.1-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/home/app/web

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN addgroup -S app && adduser -S app -G app

RUN apk update && \
    apk add --no-cache build-base gcc python3-dev libpq-dev bash

RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --dev --system --deploy --ignore-pipfile

COPY . $APP_HOME
COPY docker/startup.sh .

RUN chown -R app:app $APP_HOME
RUN chmod +w $APP_HOME/bcoin/apps/coins/migrations
RUN chmod +x startup.sh

USER app

EXPOSE 8000

CMD $APP_HOME/startup.sh
