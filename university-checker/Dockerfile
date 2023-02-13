FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /home/morzan/university-checker-master/university-checker/
COPY  . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uwsgi", "--master", "--ini", "/opt/conf/mysite_uwsgi.ini"]
