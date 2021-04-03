FROM python:3.8

RUN mkdir /var/www
WORKDIR /var/www

COPY Pipfile ./

RUN pip install pipenv
RUN pipenv install --system

CMD ["pipenv", "run", "start"]
