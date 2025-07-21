# Use slim image to reduce size
FROM python:3.10-slim

# Disable .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Explicitly disable GPU usage (to avoid unnecessary CUDA memory allocation)
ENV CUDA_VISIBLE_DEVICES=""

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the app port
EXPOSE 5000

# Run using Gunicorn for production-like behavior (optional, can switch to `python app.py`)
CMD ["python", "app.py"]