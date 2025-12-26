FROM python:3.11-slim
COPY . .
WORKDIR /app

RUN pip install flask &&\
    pip install psycopg2-binary
    
CMD ["python", "app.py"]