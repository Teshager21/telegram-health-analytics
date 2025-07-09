FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY api/ ./api/

COPY src/ ./src/

CMD ["python", "api/main.py"]
