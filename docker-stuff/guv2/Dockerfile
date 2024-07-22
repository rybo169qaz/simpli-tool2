# based upon (Medum) Live Video Streaming using Docker
#   https://medium.com/@gosranineeramar/live-video-streaming-using-docker-199dd9eb961a 

# Use a base image with a lightweight Linux distribution
FROM ubuntu:22.04

# Install required dependencies for guvcview
RUN apt-get update && apt-get install -y \
guvcview \
libgl1-mesa-glx \
libgstreamer1.0-0 \
libgstreamer-plugins-base1.0-0 \
pulseaudio-utils

#RUN apt-get update && apt-get install -y zlib-dev jpeg-dev gcc musl-dev

RUN apt-get update && apt-get install -y python3 python3-pip 
#RUN apt-get update && apt-get install -y build-dep python-imaging
#RUN apt-get update && apt-get install -y python3-opencv
RUN pip list

#RUN pip install pypng zbar pillow 
##RUN pip install python-qrtools
#RUN pip install qrtools
RUN pip install segno 
##RUN pip install pyzbar
##RUN pip install Pillow
##RUN pip install Image
#RUN pip install opencv-contrib-python
RUN pip list

RUN mkdir -p /app

COPY doit.sh /app/doit.sh
RUN chmod ugo+x /app/doit.sh

COPY convert.py /app/convert.py

# Set the entrypoint to guvcview
#ENTRYPOINT ["guvcview", "--no_display"]  # it appears this invalid now
#ENTRYPOINT ["guvcview", "--verbosity=2 --gui=none"]
ENTRYPOINT ["/bin/sh"]
