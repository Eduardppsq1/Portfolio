FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9999

RUN pip install mysql-connector-python

CMD [ "python", "app2.py" ]
