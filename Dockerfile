# ChatGPT Sora 2 Automation - Dockerfile
# Build automation environment with Chrome and Python

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -q --continue -P /tmp "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /usr/local/bin/chromedriver

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY automation.py .
COPY config.json.example ./config.json.example

# Create directories
RUN mkdir -p /app/videos /app/logs

# Environment variables (override these at runtime)
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Note: Mount config.json and credentials.json at runtime
# docker run -v $(pwd)/config.json:/app/config.json \
#            -v $(pwd)/credentials.json:/app/credentials.json \
#            chatgpt-sora2-automation

# Run the automation
CMD ["python", "automation.py"]
