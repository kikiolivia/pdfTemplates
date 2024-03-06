FROM python:3.9-slim

ENV TZ="Asia/Jakarta"
ENV PYTHONUNBUFFERED=1

WORKDIR /root/code

ADD . .

RUN date

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 4444

CMD [ "python", "./main.py" ]