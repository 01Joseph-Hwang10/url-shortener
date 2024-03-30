FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN pw_migrate migrate --directory db/migrations --database sqlite:///db/db.sqlite3

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
