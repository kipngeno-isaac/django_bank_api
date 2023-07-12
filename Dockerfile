# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt /code/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . /code/

# Expose the port on which the Django app will run
EXPOSE 8000

# Set the environment variables
ENV MYSQL_HOST=mysql
ENV MYSQL_PORT=3306
ENV MYSQL_DATABASE=bankapidb
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=54985498

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
