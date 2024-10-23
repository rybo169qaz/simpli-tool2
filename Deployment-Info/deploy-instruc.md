# Deployment Insutrcutions
This contains instructions for preparing the target platforms to run the simpliplay software suite.

## Reference document

Installing Ansible

## Getting Ansible


### Enable SSH

- Installation of python packages
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
    - **cd simpli-tools2 **
- Copy the file over
    - **rsync -r Deployment-Info robert@*IpAddress*:/tmp **
    - e.g. **rsync -r Deployment-Info robert@192.168.0.49:/tmp **
- TBD

#### On client

- Install primary controller tools
    - **sudo apt install -y rsync retext less **
    - 

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
        - **sudo apt install -y python3-pip **
        - **sudo apt install -y pipx **

### INSTALLING ANSIBLE


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
    - FOR UPGRADE LATER **sudo pipx upgrade --include-injected ansible **
    - **pipx inject ansible argcomplete **

#### Checking version of ansible
- **ansible --version **


## Software needed on the client

- This should be included in the ansible config, but is currently done manually

- Increasing the volume on the device
    - 
    - On some devices (e.g. zotac) it has been found that the volume is far too low despite adjustment of the user volume control. For that reason an ibvestigation as to how to raise the volume was sought and found.
    - 
    - See Ref: [(Superuser): Can i increase the sound volume above 100% in Linux](https://superuser.com/questions/300178/can-i-increase-the-sound-volume-above-100-in-linux)
    - Install the software
        - **sudo apt-get install -y pulseaudio pavucontrol **
        - **sudo shutdown --reboot **    (Necessary for the module to take effect)

    - Now change the setting to double the volume to 200
        - **pactl list | grep -oP 'Sink #\K([0-9]+)' | while read -r i ; do pactl -- set-sink-volume $i 200 ; done **
    - zzz

- Enable TeamViewer
    - See [Install TeamViewer (Classic) on Linux without graphical user interface](https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-classic/installation/linux/install-teamviewer-classic-on-linux-without-graphical-user-interface/)

- Installing zoom
    - See the ansible files
    - download 
    - sudo apt install ./zoom_amd64.deb
    - sudo apt --fix-broken install
    - 

- Other

somme blurb

more blurb
