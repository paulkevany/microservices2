FROM python:3-stretch

WORKDIR /app

COPY webclient.py requirements.txt /app/
COPY templates /app/templates

RUN pip install -r requirements.txt

EXPOSE 8080:5000

CMD ["python", "webclient.py"]
