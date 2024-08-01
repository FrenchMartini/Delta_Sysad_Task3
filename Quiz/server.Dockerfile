FROM python:3.9

WORKDIR /app

COPY server.py /app/server.py
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh



RUN pip install --upgrade pip
RUN pip3 install psycopg2-binary

CMD ["wait-for-it.sh", "db:5432", "--", "python", "server.py"]