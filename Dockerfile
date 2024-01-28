FROM python:3.9

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install

COPY . /app/
ENTRYPOINT ["pipenv", "run", "start"]
