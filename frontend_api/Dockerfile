# Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire app into the container
COPY . .

# Command to run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
