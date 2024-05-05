FROM python:3.9-slim

WORKDIR /app

COPY ./main.py /app
COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

CMD ["python", "main.py"]
