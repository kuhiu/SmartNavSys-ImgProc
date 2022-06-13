ARMCC_PREFIX=${HOME}/toolchains/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
LIBS = 	-lopencv_core -lopencv_imgproc -lopencv_imgcodecs \
		-lopencv_highgui -lopencv_calib3d -lopencv_features2d \
		-lopencv_flann -lopencv_ml -lopencv_objdetect -lopencv_photo \
		-lopencv_superres -lopencv_video -lopencv_videostab -lopencv_videoio -pthread 

all:
	$(ARMCC_PREFIX)g++ main.cpp -g -o main.bin \
	-I../OpenCvOnZybo/opencv/buildCross/installation/include \
	-L../OpenCvOnZybo/opencv/buildCross/installation/lib \
	$(LIBS)
	
asd:	
	-lopencv_highgui -lopencv_calib3d -lopencv_features2d \
	-lopencv_flann -lopencv_ml -lopencv_objdetect -lopencv_photo -lopencv_stitching \
	-lopencv_superres -lopencv_video -lopencv_videostab -lopencv_videoio \
