#ARMCC_PREFIX=${HOME}/toolchains/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
ARMCC_PREFIX=/usr/bin/arm-linux-gnueabihf-
LIBS = 	-lopencv_core -lopencv_imgproc -lopencv_imgcodecs \
		-lopencv_highgui -lopencv_calib3d -lopencv_features2d \
		-lopencv_flann -lopencv_ml -lopencv_objdetect -lopencv_photo \
		-lopencv_superres -lopencv_video -lopencv_videostab -lopencv_videoio -pthread \
		-ltensorflowlite_c 
LIB_DIR = -L/opencv/buildCross/installation/lib -L./tensorflow/tflite_build 
INC_DIR = -I/opencv/buildCross/installation/include -I./include

all:
	$(ARMCC_PREFIX)g++ --version
	$(ARMCC_PREFIX)g++ -std=c++0x -std=c++11 -o main.bin main.cpp func.cpp $(LIBS) $(LIB_DIR) $(INC_DIR)

save:
	arm-none-eabi-g++ -o main.bin main.cpp -ltensorflowlite_c -L. -I./include