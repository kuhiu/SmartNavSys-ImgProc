// C++ program for the above approach
#include <iostream>
#include <numeric>
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

int getMaxAreaContourId(std::vector <std::vector<cv::Point> > contours) {
    double maxArea = 0;
    int maxAreaContourId = -1;
    for (int j = 0; j < contours.size(); j++) {
        double newArea = cv::contourArea(contours.at(j));
        if (newArea > maxArea) {
            maxArea = newArea;
            maxAreaContourId = j;
        } // End if
    } // End for
    return maxAreaContourId;
} // End function

// Driver code
int main(int argc, char** argv)
{
    int i,j;
    int mem_fd;
    void *img_read = NULL;
    void *img_write = NULL;
    cv::Mat img, img_hsv, img_bgr;
    cv::Scalar uper_green, lower_green, x_avg;
    cv::Mat green_mask, points;
    std::vector<std::vector<cv::Point> > green_contours;
    std::vector<cv::Point> largest_contour;
    cv::Scalar font_Color(255, 255, 255, 255);

    // Measure time
    struct timespec begin, end; 

    int largest_area=0;
    int largest_contour_index=0;

    int cX, cY;
    cv::Moments M;

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

    uper_green = cv::Scalar(90,255,255);
    lower_green = cv::Scalar(20,100,100);

    while(1){
        // Read mem address 
        memcpy(img.data, img_read, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);

        // Start measuring time 
        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &begin);

        // Get HSV image
        cv::cvtColor(img, img_bgr, cv::COLOR_RGBA2BGR);
        cv::cvtColor(img_bgr, img_hsv, cv::COLOR_BGR2HSV);

        // Mask
        cv::inRange(img_hsv, lower_green, uper_green, green_mask);

        // Find Contours
        cv::findContours(green_mask, green_contours, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);

        for( size_t i = 0; i< green_contours.size(); i++ ) // iterate through each contour.
        {
            double area = cv::contourArea( green_contours[i] );  //  Find the area of contour

            if( area > largest_area )
            {
                largest_area = area;
                largest_contour_index = i;               //Store the index of largest contour
                //bounding_rect = cv::boundingRect( green_contours[i] ); // Find the bounding rectangle for biggest contour
            }
        }
        // Largest contour
        largest_contour = green_contours[largest_contour_index];

        // Draw largest contour
        cv::drawContours(img, green_contours, largest_contour_index, cv::Scalar(0,0,0,255), 2);

        // Center of the contour
        M = cv::moments(largest_contour);
	    cX = int(M.m10 / M.m00);
	    cY = int(M.m01 / M.m00);

        // Draw center of area
        cv::circle(img, cv::Point(cX, cY), 7, (255, 255, 255, 255), -1);

        // Stop measuring time and calculate the elapsed time
        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
        long seconds = end.tv_sec - begin.tv_sec;
        long nanoseconds = end.tv_nsec - begin.tv_nsec;
        double elapsed = seconds + nanoseconds*1e-9;

        // Write time elapsed on image
        cv::putText(img, std::to_string(elapsed), cv::Point(100,220), cv::FONT_HERSHEY_TRIPLEX, 0.5, font_Color, 1);

        // Write mem address 
        memcpy(img_write, img.data, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);

        largest_area = 0;
    }

    return 0;
}