# Dockerfile for Django
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
CMD ["/wait-for-it.sh", "db:3306", "-t", "60", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]