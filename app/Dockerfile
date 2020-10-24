FROM python:3.8

RUN mkdir /var/www
WORKDIR /var/www

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run", "--port=3031", "--host=0.0.0.0"]