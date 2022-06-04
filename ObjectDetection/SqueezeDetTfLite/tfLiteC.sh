printf "Cloning Tensorflow repo..."
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
git checkout v2.6.0

printf "Creating tflite_build folder...\n"
mkdir -p tflite_build gen/armv7/cpp
cd tflite_build

ARMCC_FLAGS="-march=armv7-a -mfpu=neon-vfpv3 -funsafe-math-optimizations -mfp16-format=ieee"
ARMCC_PREFIX=${HOME}/toolchains/gcc-arm-8.3-2019.03-x86_64-arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
cmake -DCMAKE_C_COMPILER=${ARMCC_PREFIX}gcc \
  -DCMAKE_CXX_COMPILER=${ARMCC_PREFIX}g++ \
  -DCMAKE_C_FLAGS="${ARMCC_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${ARMCC_FLAGS}" \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_SYSTEM_NAME=Linux \
  -DCMAKE_SYSTEM_PROCESSOR=armv7 \
  -DCMAKE_SYSROOT=/home/martin/Escritorio/Tesis/Petalinux_Projects/Imagen/build/tmp/work/plnx_zynq7-xilinx-linux-gnueabi/linux-xlnx/4.19-xilinx-v2019.1+gitAUTOINC+9811303824-r0/recipe-sysroot \
  ../tensorflow/lite/c

cmake --build . -j$(nproc)

#  #-DCMAKE_SYSROOT=/home/martin/Escritorio/Tesis/Petalinux_Projects/Imagen/build/tmp/work/plnx_zynq7-xilinx-linux-gnueabi/linux-xlnx/4.19-xilinx-v2019.1+gitAUTOINC+9811303824-r0/recipe-sysroot \

#cp libtensorflowlite* ../gen/armv7/c
#cd ../..
#rm -r tflite_build
#rm -r tensorflow