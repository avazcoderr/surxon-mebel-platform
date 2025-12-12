# Python runtime as parent image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system build dependencies (gcc, libpq-dev, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*  # Remove apt lists immediately to keep this layer clean

# Install Python dependencies
COPY ./surxon_backend/requirements.txt .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings

RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY ./docker/entrypoint.sh ./docker/entrypoint.sh
RUN chmod +x ./docker/entrypoint.sh

# Copy project
COPY . .

# Set work directory to the backend folder
WORKDIR /app/surxon_backend

# Create staticfiles directory
RUN mkdir -p /app/surxon_backend/static
RUN mkdir -p /app/surxon_backend/staticfiles

# Expose port (Railway will use PORT environment variable)
EXPOSE 8000

# Use entrypoint script for Railway
CMD ["/app/docker/entrypoint.sh"]