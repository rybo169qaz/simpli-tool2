# Deployment Insutrcutions
This contains instructions for preparing the target platforms to run the simpliplay software suite.

## Reference document

Installing Ansible

## Getting Ansible


### Enable SSH

- Enabling SSH
    - **sudo apt-get update**
    - **sudo apt-get upgrade**
    - **sudo apt-get install -y openssh-server **
    - DEPRECATED **sudo apt-get install openssh-client**
    - **sudo systemctl enable ssh**
    - **ip -4 a**
        - Note the ip address

- In examples below let us assume that 
    - ipAddress == 192.168.0.49
    - userName == robert
    - password == p

- use of ssh
    - ssh *userName*@*ipAddress*
    - e.g. **ssh robert@192.168.0.49**

### Copy the document for reading

#### On controller

- Install primary controller tools
    - **sudo apt install -y rsync retext **
- Move to the root of the repo
    - **cd ~/PROJ2/SIMPLI-TOOL/GIT-REPO/simpli-tool2 **
- Copy the file over
    - **rsync -r Deployment-Info robert@*IpAddress*:/tmp **
    - e.g. **rsync -r Deployment-Info robert@192.168.0.49:/tmp **
- TBD

#### On client

Do the following via an SSH session 

- Install primary controller tools
    - **sudo apt install -y rsync retext less **
   

- Obtain the principle artifacts/documents
    - **cd ~ **
    - **cp -r /tmp/Deployment-Info/ . **
    - To read the document
        - **cd Deployment-Info **
        - If on device with (Graphical) Desktop
            - **retext deploy-instruc.md **
        - If on terminal
            - **less deploy-instruc.md **

### Update Python interpeter to correct version
- See - Reference [(HowToGeek) How to Install the Latest Python Version on Ubuntu Linux](https://www.howtogeek.com/install-latest-python-version-on-ubuntu/)


- Steps
    - **sudo apt install -y python3.12 **

- Check
    - **python3 --version **
    - should return 3.12.x


### Installing PIP stuff
- Follow these instructions (using the pipx variant) 
    - [(ansible) Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible-with-pip)
    - Install python3-pip
        - Installing pip (python3-pip) did not work on the Wyse devices with Mint)
    - NEW
        - **DEPR sudo apt install -y python3-pip **
        - **sudo apt install -y pipx **

### ANSIBLE

### Get ansible installed
- See reference [How To Install and Configure Ansible on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04)

#### Configuring Control Node (Ubuntu)
- **sudo apt-add-repository ppa:ansible/ansible **
- **sudo apt update **
- **sudo apt install ansible **


#### Configuring Client Node
  - It was necessary to use pipx on debian mint on zotac
  - **pipx ensurepath **
  - **pipx install --include-deps ansible **
  - **pipx inject ansible argcomplete **
  - FOR UPGRADE LATER **sudo pipx upgrade --include-injected ansible **

#### Checking version of ansible
- **ansible --version **


### Using Ansible

- Useful [spacelift - Ansible Tutorial for Beginners: Ultimate Playbook & Examples](https://spacelift.io/blog/ansible-tutorial)
- General syntax
    - ansible [host-pattern] -m [module] -a “[module options]”

#### Ad-hoc ansible

- `ansible -i <inventory-file> --ask-pass <node-set-identity> <command>`
- e.g. 
    - `cd ~/PROJ2/SIMPLI-TOOL/GIT-REPO/simpli-tool2/Deployment-Info/Ansible-stuff`
    - `ansible -i inv --ask-pass zbox -m ping`

### Playbook ansible

- `ansible -i <inventory-file> <playbook>`
- ansible [host-pattern] -m [module] -a “[module options]”
- e.g. 
    - `cd ~/PROJ2/SIMPLI-TOOL/GIT-REPO/simpli-tool2/Deployment-Info/Ansible-stuff`
    - `ansible -i inv --ask-pass zbox -m ping`

## Software needed on the client

- This should be included in the ansible config, but is currently done manually

### VOLUME CONTROL
- Increasing the volume on the device
    - 
    - On some devices (e.g. zotac) it has been found that the volume is far too low despite adjustment of the user volume control. For that reason an ibvestigation as to how to raise the volume was sought and found.
    - 
    - See Ref: [(Superuser): Can i increase the sound volume above 100% in Linux](https://superuser.com/questions/300178/can-i-increase-the-sound-volume-above-100-in-linux)
    - Install the software
        - **sudo apt-get install -y pulseaudio pavucontrol **
        - **sudo shutdown --reboot **    (Necessary for the module to take effect)


    - To get the channel volume use 
        - `pactl -- get-sink-volume <channel-id>`
    - To set the channel volume use 
        -  You can use an abolsute or percentage. Prefer use percentage.
        - `pactl -- set-sink-volume <channel-id> <volume>% `

    - Now change the setting to double the volume to 200
        - **pactl list | grep -oP 'Sink #\K([0-9]+)' | while read -r i ; do pactl -- set-sink-volume $i 200 ; done **
    - Note
        - A) This caused a poblem for Wyse devices as sound came out of onboard speaker
        - B I observed that if i look at all sinks
            - `pactl list sinks`
            - that the sink has a property called alsa.card_name which contains the word HDMI
            - 

### Remote Access Software

#### AnyDesk
- This is preferred above TeamViewer.
- Enable AnyDesk
   - see [AnyDesk Home] (https://anydesk.com)
   - [AnyDesk Help Center](https://support.anydesk.com/knowledge)
   - [download Linux](https://anydesk.com/en-gb/downloads/linux)
   - [AnyDesk DEB repository how-to](http://deb.anydesk.com/howto.html) : suggest use this manually
   - [Downlaod Ubuntu Mint](https://anydesk.com/en-gb/downloads/thank-you?dv=deb_64)
   - [AnyDesk Command-Line Interface for Linux](https://support.anydesk.com/knowledge/command-line-interface-for-linux)

#### TeamViewer
- This is deprecated as AnyDesk has fewer problems with licensing.
- Enable TeamViewer
    - See [Install TeamViewer (Classic) on Linux without graphical user interface](https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-classic/installation/linux/install-teamviewer-classic-on-linux-without-graphical-user-interface/)

#### ZOOM
- See instructions [Installing or updating Zoom on Linux](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063458#h_89c268b4-2a68-4e4c-882f-441e374b87cb)
- Installing zoom
    - See the ansible file **Deployment-Info/Ansible-stuff/zoom.yml**
    - I had to do an **apt-get upgrade **
    - **sudo apt install ./zoom_amd64.deb **
    - **sudo apt --fix-broken install **
    - 

### ENVIRONMENT

#### LIGHTDM
- Use **gsettings ** to set them programmatically.
- To enable automatic login use 
    - [LightDM : Setting an Automatic Login](https://wiki.ubuntu.com/LightDM)
    - Specifically edit **/etc/lightdm/lightdm.conf.d/01_my.conf**
    - Add lines
        - **autologin-user=robert**
        - **autologin-user-timeout=7**


### OTHER B
- Other

somme blurb

more blurb