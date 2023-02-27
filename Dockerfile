FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
