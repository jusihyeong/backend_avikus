FROM python:3.9.12

COPY . /backend

RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.txt
RUN pip install mysqlclient
EXPOSE 8000

WORKDIR /backend

CMD sleep 5 && python main.py