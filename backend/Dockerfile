FROM python:3.12-slim


# Install system dependencies including ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -ms /bin/bash appuser
WORKDIR /app



# Copy backend source code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt


# Expose backend port
EXPOSE 8000

# Define app module (file:object)
ENV APP_MODULE=main:app \
    HOST=0.0.0.0 \
    PORT=8000

# Start FastAPI with Uvicorn (development-style run, simpler than Gunicorn)
CMD uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT"
