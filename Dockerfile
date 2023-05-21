# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY main.py .
COPY src/m3u_transform.py .

# Set the entry point command for the container
CMD ["python", "main.py"]