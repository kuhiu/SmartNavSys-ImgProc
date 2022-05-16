# Open CV on zybo (PoC)

PoC using png server app.

# Reference 

https://github.com/jinchenglee/zybo_linux_setup_doc

# Install toolchain

sudo apt-get update
sudo apt-get install -y build-essential sshpass cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libgtk-3-dev libcanberra-gtk* libatlas-base-dev gfortran python2.7-dev python3-dev
sudo pip install numpy
sudo apt-get install -y gcc-arm-linux-gnueabihf  g++-arm-linux-gnueabihf

# Edit cross compiler for opencv to 4.9

Edit on opencv/platforms/linux/arm-gnueabi.toolchain.cmake

Note: Use 4.9 cross compiler version.

# Error loading shared libraries 

save opencv.conf file on /etc/ld.so.conf.d/ and run "sudo ldconfig -v"
