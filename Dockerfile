FROM python:3.8

#ENV key=value

ADD app.py .

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install -r /tmp/requirements.txt

CMD [ "python", "./app.py" ]