# Dockerfile for Django
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN curl -o /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "db:3306", "-t", "60", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]