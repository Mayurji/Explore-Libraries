# Dockerfile
# Defines the steps to build a self-contained container image
# for the FastAPI ML application.

# 1. Base Image: Use a lightweight official Python image
FROM python:3.11-slim

# 2. Set Working Directory inside the container
WORKDIR /app

# 3. Install Dependencies
# Copy requirements file first for Docker layer caching optimization
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Application Files and Model
# Copy the trained model and the main application code
COPY iris_model.pkl .
COPY main.py .

# 5. Expose the port the application runs on
EXPOSE 8000

# 6. Run the Application
# Use the Uvicorn ASGI server to start the FastAPI application
# The exec form (JSON array) is preferred for signal handling and graceful shutdown.
# Command: uvicorn main:app --host 0.0.0.0 --port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
