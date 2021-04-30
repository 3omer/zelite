FROM python:3.6-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt 
RUN pip install gunicorn[gevent]

# copy code
COPY . .

EXPOSE 5000

CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 main:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info