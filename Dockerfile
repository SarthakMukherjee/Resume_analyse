FROM python:3.10-slim

WORKDIR /code

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY ./backend/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements.txt

# Copy project files
COPY . .

# Allow imports from backend directory
ENV PYTHONPATH=/code/backend

# Expose FastAPI port
EXPOSE 7860

# Seed admin and start API
# CMD uvicorn backend main:app --host 0.0.0.0 --port 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

