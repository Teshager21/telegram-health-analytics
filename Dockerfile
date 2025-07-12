# Use official Python slim image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install OS-level deps if needed
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Default to bash for dev container
CMD ["/bin/bash"]
