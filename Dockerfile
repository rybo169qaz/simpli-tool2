# See    How to Create Docker Images?
#        https://kodekloud.com/blog/create-docker-images/

# See    Docker: adding a file from a parent directory
#        https://stackoverflow.com/questions/24537340/docker-adding-a-file-from-a-parent-directory

FROM python:latest
RUN mkdir -p /app
WORKDIR /app
COPY MySimpleApp/pyplay /app/pyplay
COPY MySimpleApp/play.sh /app
RUN apt-get update
RUN apt-get install -y \
    libzbar0 \
    vlc \
    chromium \
    ffmpeg 
RUN pwd
RUN ls
RUN pip list
#RUN pip install flask
RUN pip install pyzbar
RUN pip install pillow
RUN pip list
#ENTRYPOINT ["/bin/sh"]
ENTRYPOINT ["/app/play.sh"]
