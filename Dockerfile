FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask flask-sqlalchemy

EXPOSE 5000

CMD ["python", "app.py"]