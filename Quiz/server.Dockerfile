FROM python:3.9

WORKDIR /app

COPY server.py /app/server.py


RUN pip install --upgrade pip
RUN pip3 install psycopg2-binary

CMD [ "python3" , "server.py" ] 