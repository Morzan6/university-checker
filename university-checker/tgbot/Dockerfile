FROM python:3.9

ENV PYTHONUNBUFFERED=1


WORKDIR /opt/app/tgbot

COPY  . .

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 main.py

