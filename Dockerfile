# Specify the base image with preinstalled python and other packages
FROM python:3.9.14-slim

# We copy our sources and start the project in this path inside the container
WORKDIR /app

# Install the server that will run our app because `flask run` is only for development purposes
RUN pip3 install gunicorn

# Firstly, install dependencies to have them in a docker layer separated from source code
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

# Copy source code
COPY . .

# Publish the gunicorn's port to the outside world
EXPOSE 5001

# Start the web server using production server Gunicorn
ENTRYPOINT ["gunicorn", "app:app", "--workers=1", "--bind=0.0.0.0:5001"]