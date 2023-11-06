FROM python:3.10-slim

WORKDIR /app

RUN apt update -y
RUN pip install -U pip

# Install serving packages
RUN pip install -U fastapi==0.103.2 uvicorn==0.15.0 validators==0.22.0

# Container commands
RUN apt update -y
RUN apt install -y git


# Install python dependencies
RUN pip install torch==2.0.1

# Copy in files
COPY ./ ./
COPY ./examples/docker/multi_inputs/ ./


# Remove eventually
RUN pip install ./

ENV PIPELINE_PATH=my_pipeline:pipeline_graph
ENV PIPELINE_NAME=plutopulp/multi-inputs
ENV PIPELINE_IMAGE=plutopulp/multi-inputs

CMD ["uvicorn", "pipeline.container.startup:create_app", "--host", "0.0.0.0", "--port", "14300"]
