# Use official Python image as base (slim version for reduced size)
FROM python:3.11-slim
# Set working directory
WORKDIR /app
# Copy only requirements first to leverage Docker caching
COPY ./requirements.txt .
# Install dependencies with pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# Copy application files
COPY . .
# Expose FastAPI default port
EXPOSE 8000
# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
