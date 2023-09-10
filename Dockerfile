FROM python:3.10

WORKDIR /barcode-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./main.py"]