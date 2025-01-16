FROM python:3.10.2

# Set the working directory inside the container
WORKDIR /code

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/code/src

# Copy requirements.txt from the project root
COPY containers/pipelinerunner/requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install -r /code/requirements.txt

# Copy the entire project directory into the container
COPY . /code/

# Run the ETL script
CMD ["python", "/code/src/etl.py"]
