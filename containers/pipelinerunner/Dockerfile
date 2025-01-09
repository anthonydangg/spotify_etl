FROM python:3.10.2

WORKDIR /code
ENV PYTHONPATH=/code/src
#maybe unsure of env

ADD ./containers/pipelinerunner/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ /code/
#applies where build directory is ran to paste into docker dir

CMD ["python", "./src/etl.py"]