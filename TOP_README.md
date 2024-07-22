# simpli-play2 FULL development
This contains 
+ Code for the SimpliPlay2
+ Packaging tool for SimplPlay2 (creates a single executable)
+ Docker framework to run SimpliPlay2


## SimpliPlay2 Code

This is the python codebase together with invoking 
scripts (bash and CMD).
Currently I am unsure whether it is actually configured 
correctly as a package.
It requires a number of packages to be installed on the system.

Currently the SimpliPlay2 can play text media. This is included as 
it will allow simple tests to be automated.
By contrast testing the creation of audio or video is very difficult.

## SimpliPlay2 Packager

This creates a standalone binary (windows and linux) that can be 
downloaded and run.
It contains all the necessary Python Packages so that it can run 
without OS requirements.

## SimplPlay2 Docker framework

This contains the Config and Image specs required to run the SimplPlay2 
package in.
This enables the tool to be run without requiring any host OS 
changes (other than of installing Docker).
The purpose of this is to enable local testing without impacting the 
host PC.
At the time of writing the project invokes one of two media 
players (VLC or FFMPEG). 
They are assumed to have fixed locations. 
Obviously when using docker we only have a file and network connection to 
the container.
It may therefore be a be a good approach to try to render the media in a browser.
Using this approach we can use a simple network connection.
The difference however is that currently we launch the media player (e.g. VLC) whereas 
if we use docker then we can only point the platform device (e.g. browser) 
to the port of the docker container.  