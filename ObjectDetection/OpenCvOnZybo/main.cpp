// C++ program for the above approach
#include <iostream>
#include <opencv2/opencv.hpp>
#include <sys/mman.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

using namespace cv;
using namespace std;

#define FRAMEBUFFER_READ_OFFSET  0x01000000  // Image ram position
#define IMG_WIDTH                 320   // Image size
#define IMG_HEIGHT                240
#define IMG_CHANNEL                 4
#define FILE_NAME "test.png"

// Driver code
int main(int argc, char** argv)
{
    int i,j;
    int mem_fd;
    void *img_read = NULL;
    Mat img;


    mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
    if ( mem_fd == -1)
    {
        printf("Open /dev/mem Failed\n");
        return -1;
    }

    img_read = mmap(NULL, IMG_WIDTH*IMG_HEIGHT*4, PROT_READ | PROT_WRITE, MAP_SHARED, mem_fd, (off_t)FRAMEBUFFER_READ_OFFSET );	// phys_addr should be page-aligned.	

    if(img_read == MAP_FAILED){
        printf("Mapping Failed\n");
        printf("Oh dear, something went wrong with read()! %s\n", strerror(errno));
        return -1;
    }

    img.create(IMG_HEIGHT,IMG_WIDTH,CV_8UC4);
    memcpy(img.data, img_read, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);
    cvtColor(img, img, COLOR_RGBA2BGRA);
    imwrite(FILE_NAME, img);
    return 0;
}