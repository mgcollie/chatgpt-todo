# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Create a non-root user
RUN useradd --create-home appuser

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD --chown=appuser:appuser . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER appuser

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
