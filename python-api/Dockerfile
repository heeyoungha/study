FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY entrypoint.sh /entrypoint.sh
COPY . .
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"] 