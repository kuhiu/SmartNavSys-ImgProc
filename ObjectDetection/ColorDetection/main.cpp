// C++ program for the above approach
#include <iostream>
#include <opencv2/opencv.hpp>
#include <sys/mman.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define FRAMEBUFFER_READ_OFFSET   0x01000000  // Image ram position
#define FRAMEBUFFER_WRITE_OFFSET  0x02000000  // Image ram position
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
    void *img_write = NULL;
    cv::Mat img, img_hsv, img_bgr;
    cv::Scalar uper_green, lower_green;
    cv::Mat green_mask;
    std::vector<std::vector<cv::Point> > green_contours;

    // Measure time
    struct timespec begin, end; 

    mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
    if ( mem_fd == -1)
    {
        printf("Open /dev/mem Failed\n");
        return -1;
    }

    img_read = mmap(NULL, IMG_WIDTH*IMG_HEIGHT*IMG_CHANNEL, PROT_READ | PROT_WRITE, MAP_SHARED, mem_fd, (off_t)FRAMEBUFFER_READ_OFFSET );	// phys_addr should be page-aligned.	

    if(img_read == MAP_FAILED){
        printf("Mapping Failed\n");
        printf("Oh dear, something went wrong with read()! %s\n", strerror(errno));
        return -1;
    }

    img_write = mmap(NULL, IMG_WIDTH*IMG_HEIGHT*IMG_CHANNEL, PROT_READ | PROT_WRITE, MAP_SHARED, mem_fd, (off_t)FRAMEBUFFER_WRITE_OFFSET );	// phys_addr should be page-aligned.	

    if(img_write == MAP_FAILED){
        printf("Mapping Failed\n");
        printf("Oh dear, something went wrong with read()! %s\n", strerror(errno));
        return 1;
    }

    img.create(IMG_HEIGHT,IMG_WIDTH,CV_8UC4);

    uper_green = cv::Scalar(80,255,255);
    lower_green = cv::Scalar(30,100,100);

    while(1){
        // Read mem address 
        memcpy(img.data, img_read, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);

        // Start measuring time 
        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &begin);

        cv::cvtColor(img, img_bgr, cv::COLOR_RGBA2BGR);
        cv::cvtColor(img_bgr, img_hsv, cv::COLOR_BGR2HSV);

        // 
        cv::inRange(img_hsv, lower_green, uper_green, green_mask);

        //
        cv::findContours(green_mask, green_contours, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);

        // Draw contours
        cv::drawContours(img, green_contours, -1, cv::Scalar(0,0,0,255), 2);

        // Stop measuring time and calculate the elapsed time
        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
        long seconds = end.tv_sec - begin.tv_sec;
        long nanoseconds = end.tv_nsec - begin.tv_nsec;
        double elapsed = seconds + nanoseconds*1e-9;
        //printf("Time executing.. %f \n", elapsed);

        // Write time elapsed on image
        cv::Scalar font_Color(255, 255, 255, 255);
        cv::putText(img, std::to_string(elapsed), cv::Point(100,220), cv::FONT_HERSHEY_TRIPLEX, 0.5, font_Color, 1);

        // Write mem address 
        memcpy(img_write, img.data, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);
    }

    return 0;
}