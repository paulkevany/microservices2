FROM python:3-stretch

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 50051

CMD ["python", "greeter_server.py"]
