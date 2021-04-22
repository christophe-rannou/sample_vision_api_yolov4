FROM python:3.7.10-slim-buster

WORKDIR /python

# Include relevant files
ADD src /python/src
ADD requirements.txt /python/requirements.txt
ADD resources/coco.names /python/resources/coco.names
ADD resources/yolov4_anchors.txt /python/resources/yolov4_anchors.txt
ADD resources/yolov4.onnx /python/resources/yolov4.onnx

# Install dependencies
RUN apt-get update && apt-get install -y python3-opencv && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

# Start the web service
CMD cd src  && python api.py


