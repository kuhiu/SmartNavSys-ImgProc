#include <stdio.h>
#include <cstdlib>
#include <math.h>
#include "tensorflow/lite/c/c_api.h"
#include <iostream>
#include <opencv2/opencv.hpp>
#include <sys/mman.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdlib.h>

#define modelFileName "MyModel.tflite"
#define FRAMEBUFFER_READ_OFFSET   0x01000000  // Image ram position
#define FRAMEBUFFER_WRITE_OFFSET  0x02000000  // Image ram position
#define IMG_WIDTH                 320   // Image size
#define IMG_HEIGHT                240
#define IMG_CHANNEL                 4
#define ANCHOR_PER_GRID             
#define CLASSES                     1
#define PROB_TRSH                 0.5
#define FILE_ANCHOR_BOXES       "./ANCHOR_BOX.txt"

float * softmax( float *x, int  i_width);
float * sigmoid( float *x, int  i_width);
float * anchorBox_load(char *filename);
void process_png_file(float *img, int xmin, int xmax, int ymin, int ymax);
void drawBoundingBoxOnImage(cv::Mat &image, double yMin, double xMin, double yMax, double xMax, double score, std::string label, bool scaled=true);
float * anchorBox_load(const char *filename);



/* This class filter the CNN output into [boxes, classes, scores] */
/* class Filter{
    
    private:

    public:

}; */

/* Slice prodiction, This class filter the CNN output into [pred_class_probs, pred_conf, pred_box_delta] */
/* class SlicePrediction{
    
    private:
        int num_class_probs = ANCHOR_PER_GRID * CLASSES;
    public:

}; */

/* Filter filter_output(float *cnn_output){
    Filter myfilter;

    return myfilter; 
} */