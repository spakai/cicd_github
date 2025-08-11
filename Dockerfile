# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY fib/ fib/
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default port
EXPOSE 8000

# Run the server
CMD ["python", "-m", "fib.api"]
