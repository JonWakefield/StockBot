FROM python:3.12.2-alpine3.18

ENV TZ=America/Chicago

RUN apk update

RUN addgroup -S botGroup && adduser -S -G botGroup bot

WORKDIR /app

RUN chown -R bot:botGroup /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R bot:botGroup logs && chmod -R g+rw logs

USER bot

CMD ["python", "main.py"]