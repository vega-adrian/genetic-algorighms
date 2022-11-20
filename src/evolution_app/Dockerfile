FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

RUN python app.py