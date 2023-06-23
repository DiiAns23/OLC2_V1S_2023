FROM python

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# Correr NodeJS
CMD ["python", "main.py"]