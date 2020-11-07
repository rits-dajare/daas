FROM python:3.8

RUN mkdir /var/www
WORKDIR /var/www

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system

CMD ["flask", "run", "--port=3031", "--host=0.0.0.0"]