# simpli-play2
SimpliPlay package

## History
- 3rd May : I have create a docker containert allow running of the tool for TEXT ONLY

- pre 3rd May : This provides the means to create a standalone python package (for linux or Windows)

## Overview

### SimpliPlay2 Code

This is located in **MySimpleApp** folder.
This is the python codebase together with invoking 
scripts (bash and CMD).
Currently I am unsure whether it is actually configured 
correctly as a package.
It uses a number of packages. The installation of those packages is different for the different invocation mechanisms (see later).


## Ways of execution

### Runnning directly on the linux platform

#### Overview
Runs directly on the Linux development machine.

#### Limitations
- Requires either installing packages directly on the Linux dev machine or else the creation a virtual environment.
- Requires the installaton of the appropriate media player (VLC, ffplay, chromium)


#### How to prepare
- Installation of media players
    - Install VLC
        - sudo apt install vlc
        - (possiibly use the snap?)
    - Install FFMPEG (this includes ffplay)
        - sudo apt install ffmpeg
    - Install Chromium (not Chrome)
    
- Installation of python packages
    - Preparing virtual environment
        - If using a virtual environment then 
            -  **pip install virtualenv**
            - **cd RequiredDir**
            - **virtualenv my-venv**    This creates directory my-venv
            - **source my-venv/bin.activate**
        - You will now have a prompt showing you are using my-venv
    - Install the necessary modules
        - **cd dependencies**
        - **pip install -r requirements.txt**
    - Saving new requirements (if new dependencies added)
        - **pip freeze > requirements.txt**

#### How to run
The code can be run directly from the dev machine.

- **cd MySimpleApp**
- **./play.sh  *arguments* **
- e.g.
- **./play.sh -h**         : Shows help
- Commands to build the PyInstaller package
    - **./play.sh PKGFILE**
- Commands to play media
    - **./play.sh select -p vlc -k testcountingaudio**  : To play the testcountingaudio video in VLC
    - **./play.sh select -p ffmpeg   -k testvideo** : To play the testvideo using the FFMPEG(ffplay) player.
     
    - The following are a few shortcut codes to test text, audio & video 
        - **./play.sh TT**    : Equivalent to **select -k testproverbs**
        - **./play.sh TAV**   : Equivalent to **select -p vlc -k testcountingaudio**
        - **./play.sh TVV**   : Equivalent to **select -p vlc -k testvideo**
        - **./play.sh TVC**    Equivalent to **select -p chromium -k testvideo**  
            - please note that using chromium may have a few problems
        - Convention is T [T|A|V] [C|F|V]
           - where 2nd characters is:
               - T == text 
               - A == audio 
               - V == video
           - where 3rd character is:
               - C == chromium
               - F == FFMPEG
               - V == VLC
           - 

### Using standalone Python executable using PyInstaller

#### Overview
This uses a generate image which can be moved to another machine (with same OS, same architecture)
- Reference [PyInstaller Manual](https://pyinstaller.org/en/stable/)

#### Limitations
- Requires the installaton of the appropriate media player (VLC, ffplay, chromium) on the target machine.
- Needs 

#### How to prepare
- This needs to be built on the actual Linux box WITHOUT a venv (I tried generating in a venv environment and hit problems).
- Ensure that the ./play.sh script will run and work in the Linux environment Before you use pyinstaller.
##### The basic sequence
- **pip3 install pyinstaller pyzbar**   ?other ?
- **cd MySimpleApp**
- **./play.sh PKGFILE** : This creates a binary in **MySimpleApp/dist** folder called **pkgfile** 

##### Hitting problems
- **sudo apt-get install python3-dev**
- Note A: If you get warnings about shared libraries, then try deleting the folder **pyplay/__pycache__**
- See [Python3 project remove __pycache__ folders and .pyc files](https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files)
- Note B: Article about clearing cache. I tried this to get it to build in virtualenv
- Note C: Someone else has the problem  [(TITLE)stack overflow) Pyinstaller with venv (and Pyenv installed) --> Python library not found](https://stackoverflow.com/questions/78000693/pyinstaller-with-venv-and-pyenv-installed-python-library-not-found)
- Note D: This is hopeful [(stackoverflow) Creating a pyinstaller executable that uses virtualenv imported modules](https://stackoverflow.com/questions/55228996/creating-a-pyinstaller-executable-that-uses-virtualenv-imported-modules)
- Dummy md hyperlink  [TITLE](theLink)


#### How to run
- Copy the generated **pkgfile** (as described in previous section) to the target machine.
- Execute the tool with the commands to play media (as earlier)
    - **./pkgfile  *arguments* **
    - e.g. 
        - ** ./pkgfile select -p vlc -k testcountingaudio**     (-k == --known )
        - ** ./pkgfile select -p vlc -k testvideo**

### Using a docker image (homebrewed)

#### Overview
This mounts the source code into the docker container and then runs the tool directly.

#### Limitations
Currently it can only 'play' text as it we need to do a bit to get the video/audio that is generated in docker to display on the host system. 
This is a work in progress.


#### How to prepare
- Generate docker image
    - Go to the directory where the Dockerfile is
        - ** cd simpli-play2 **
    - Create an image based on the Dockerfile. This contains all the necessary packages and mounting points.
        - The one at the top level
            - ** docker image build -t apple-image . **

#### Now run the image
- Run the tool
    - ** docker run -it --rm apple-image **
    - Note: The Dockerfile specifies /app/play.sh as the ENTRYPOINT. So this will run.

- To pass arguments to the entrypoint script, then just append them to the docker command. Thus: 
    - ** docker run -it --rm apple-image help ** 
    - ** docker run -it --rm apple-image TT ** 
    - ** docker run -it --rm apple-image select -k testtext ** 
    - ** docker run -it --rm apple-image select -k testjosephus ** 
    - ** -p vlc -u testcountingaudio ** 
    - ** docker run -it --rm apple-image select -k testvideo ** 
    - .
    - ** docker run -it --rm apple-image select --known testsilentvideo **
    - .
    - ** docker run -it --rm 
    --net=host 
    --env="DISPLAY"
    apple-image select -p ffmpeg --known testcountingaudio **  
        Note: this does not play audio 
    - ** docker run -it --rm 
    --net=host 
    --env="DISPLAY"
    apple-image select -p ffmpeg --known testsilentvideo ** 
    - ** docker run -it --rm 
    --net=host 
    --env="DISPLAY"
    apple-image select -p vlc --known testsilentvideo ** 
        - Note: It complains if you try to run this in docker as it says it should not run as root.

- To override the Entrypoint specified in the Dockerfile 
    - ** docker run -it --entrypoint /bin/sh apple-image **
    - ** docker run -it --entrypoint /app/play.sh apple-image **

- If you want to attach to an existing running container 
    - ** docker exec -it *ContainerName* /bin/sh ** 

### Experimental - using GUVCview
This is to try and get video from the docker container displayed on the host computer.
This works.

- Reference [(Medium) Live Video Streaming using Docker](https://medium.com/@gosranineeramar/live-video-streaming-using-docker-199dd9eb961a)
- Ref 2  [guvc video capture commandline](https://askubuntu.com/questions/468282/guvc-video-capture-commandline)

#### Install on host
- ** sudo apt install guvcview **

#### Create docker image
- ** cd simpli-play2/docker-stuff/guvcview-alpha **
- Now build the image
    - ** docker build -t guvcview-container . **

- Now enable docker to X11 foward
    - ** xhost +local:docker **
- Now run the image

    - ** docker run -it --rm 
    --net=host 
    --env="DISPLAY" 
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" 
    --device=/dev/video0 
    guvcview-container ** 
- You should now see the imag of the webcam.
- Now disable docker to X11 foward (it appears that this is something that should not normally persist for dev machines.
    - ** xhost -local:docker **

Also see [(Medium) Streaming Docker Containers to your Browser](https://medium.com/geekculture/streaming-docker-containers-to-your-browser-75ae9d6e27f8) (this is restricted)


### Using a docker image - using GUVCview with shell
This is to try and get video from the docker container displayed on the host computer. This one does not work.

#### How to prepare

##### Install necessary apps on host
- ** sudo apt install guvcview **

##### Create docker image
- ** cd simpli-play2/docker-stuff/guv2 **
- Now build the image
    - ** docker build -t guv2-container . **

#### How to run
- Now enable docker to X11 foward
    - ** xhost +local:docker **
- Now run the image
    - ** sudo docker run -it --rm 
    --net=host 
    --env="DISPLAY" 
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" 
    --device=/dev/video0 
    guv2-container **
- You should now see the image of the webcam.
- After copletion, disable docker to X11 foward (it appears that this is something that should not normally persist for dev machines.
    - ** xhost -local:docker **

Also see [(Medium) Streaming Docker Containers to your Browser](https://medium.com/geekculture/streaming-docker-containers-to-your-browser-75ae9d6e27f8) (this is restricted)


## Design
somme blurb

more blurb
