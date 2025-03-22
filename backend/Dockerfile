FROM python:3.9

EXPOSE 8000

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["fastapi", "dev", "./src/main.py"]