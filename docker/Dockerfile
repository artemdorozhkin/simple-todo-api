FROM python:3.8.10

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -U pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./src/app.py"]