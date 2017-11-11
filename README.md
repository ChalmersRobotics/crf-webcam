# CRF-Webcam
A webcam motion detect and anonymize for Raspberry Pi.

# Requirements
* Python2.7
* SimpleCV
* PySFTP


# Install
## Download this repo
```bash
cd
git clone https://github.com/ChalmersRobotics/crf-webcam.git
cd crf-webcam
```

## SimpleCV
* Install SimpleCV http://simplecv.readthedocs.io/en/latest/HOWTO-Install%20on%20RaspberryPi.html
```bash
sudo apt-get install ipython python-opencv python-scipy python-numpy python-setuptools python-pip
```

```bash
cd
sudo pip install https://github.com/sightmachine/SimpleCV/zipball/master
```

## Font
```bash
mkdir ~/.fonts
cd ~/crf-webcam
cp ethnocentric.ttf ~/.fonts/
```


# Configure
```bash
cd ~/crf-webcam
cp cam.conf.sample cam.conf
```
Edit cam.conf, set the parameters

