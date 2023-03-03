
FROM python:3-alpine

FROM python:3-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# ENV FLASK_APP='src/api.py'
ENV FLASK_APP='api.py'

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]