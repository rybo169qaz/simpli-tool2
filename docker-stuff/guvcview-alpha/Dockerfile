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
pulseaudio-utils \
libzbar0 \
pip

RUN pip install pyzbar
RUN pip install pillow
RUN pip list

# Set the entrypoint to guvcview
#ENTRYPOINT ["guvcview", "--no_display"]  # it appears this invalid now
ENTRYPOINT ["guvcview", "--verbosity=2 --gui=none"]
