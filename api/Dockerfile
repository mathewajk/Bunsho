# Use the Python 3 official image
# https://hub.docker.com/_/python
FROM python:3.11

# Run in unbuffered mode
ENV PYTHONUNBUFFERED=1 

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image.
COPY . ./

# Install project dependencies
RUN pip install wheel
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup.
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:gunicorn_app"]