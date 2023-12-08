FROM python:3.11.0-slim

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Update and install dependencies
RUN apt-get update && apt-get install -y gcc zlib1g-dev cmake g++ --no-install-recommends

# Copy application files
COPY requirements.txt .
COPY ./assistant/* ./assistant/

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
ENTRYPOINT ["streamlit", "run", "assistant/app.py"]