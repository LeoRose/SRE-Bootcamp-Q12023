FROM python:3-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP='src/api.py'

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
# docker run -p 8000:8000 [IMAGE_NAME]