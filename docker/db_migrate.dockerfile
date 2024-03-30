FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN pw_migrate migrate --directory db/migrations --database sqlite:///db/db.sqlite3
