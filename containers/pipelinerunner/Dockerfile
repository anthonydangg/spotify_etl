FROM python:3.10.2

# Set the working directory inside the container
WORKDIR /code

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/code/src

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy requirements.txt from the project root
COPY containers/pipelinerunner/requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install -r /code/requirements.txt

# Copy the entire project directory into the container
COPY . /code/

# Copy the cron file to the cron.d directory in the container
COPY scheduler/cron_runner /etc/cron.d/cron_runner

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron_runner

# Create the cron job
RUN crontab /etc/cron.d/cron_runner

# Log the cron output
RUN touch /var/log/cron.log

# Run the cron job/ETL script
CMD /usr/local/bin/python /code/src/etl.py && cron && tail -f /var/log/cron.log

# Run the ETL script
# CMD ["python", "/code/src/etl.py"]

# Keep the container running
# CMD ["tail", "-f", "/dev/null"]

#run tests
# CMD ["pytest"]