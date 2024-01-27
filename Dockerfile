FROM python:3.9

WORKDIR /app
COPY . /app/

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install
ENTRYPOINT ["pipenv", "run", "start"]
