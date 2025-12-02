# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# Expose the port Django runs on
EXPOSE 8001

# Run Django migrations and start the development server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8001

