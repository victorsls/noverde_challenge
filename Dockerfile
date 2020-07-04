FROM python:3.7.6

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

entrypoint ["./docker-entrypoint.sh"]