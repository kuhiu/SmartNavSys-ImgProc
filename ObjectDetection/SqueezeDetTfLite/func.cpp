#include "func.hpp"

float * softmax( float *x, int  i_width)
{
    int i;
    float max=0;
    float *e_x = (float*) malloc( i_width*sizeof(float) );
    float *output = (float*) malloc( i_width*sizeof(float) );
    // Busco el maximo del vector
    for (i = 0; i < (i_width); i++)
    {
        if ( *(x + i) > max )
            max = *(x + i);
    }

    for (i = 0; i < (i_width); i++)
        *(e_x + i) = exp( *(x + i) - max);

    // Corregir esto cuando tenemos mas de una clase.
    for (i = 0; i < (i_width); i++)
        *(output + i) = *(e_x + i) / *(e_x + i);

    //printf("output: \n");
    //printVector(output, 2700, 1, 1, 1 );

    free(e_x);
    return output;
}

float * sigmoid( float *x, int  i_width)
{
    int i;
    float *output = (float*) malloc( i_width*sizeof(float) );

    for (i = 0; i < (i_width); i++)
        *(output + i) = 1/(1+exp(- *(x + i) )) ;

    return output;
}


float * anchorBox_load(const char *filename)
{
    // Archivo
    FILE * fd;
    char s_width[100], s_height[100];
    int i_width, i_height;
    int i,j;
    size_t len = 0;
    char param[100];
    char *line = NULL;
    float *array = NULL;
    
    printf("Paso 11 \n");
    fd = fopen(filename, "r");
    printf("Paso 12 \n");
    getline(&line, &len, fd);
    printf("Paso 123 \n");
    sscanf(line, " (%[^','], %[^','])\n", s_width, s_height);
    printf("Paso 13 \n");
    i_width = atoi(s_width);  
    i_height = atoi(s_height);

    array = (float*) malloc( ( i_width*i_height) * sizeof(float));
    printf("Paso 13 \n");
    for( j=0 ; j<i_height ; j++){
        for( i=0 ; i<i_width ; i++){
            getline(&line, &len, fd);
            sscanf(line, "%s\n", param);
            *(array + i + i_width*j) = atof(param);
        } 
    }

    printf("Paso 14 \n");
    fclose(fd);
    return array;

}


void process_png_file(float *img, int xmin, int xmax, int ymin, int ymax) {
    int i, j, k;
    //printf("Xs son: %d,%d,%d,%d\n", xmax, xmin, ymax, ymin);
    for(k = 0; k < 3; k++) {
        //png_bytep row = row_pointers[y];
        for(j = 0; j < IMG_HEIGHT; j++) {
            //png_bytep px = &(row[x * 4]);
            for(i = 0; i<IMG_WIDTH; i++)
            {
                if ( (i > xmin) && (i < (xmin+5)) && (j < ymax) && (j > ymin) )
                    *(img + i + IMG_WIDTH*j + IMG_WIDTH*IMG_HEIGHT*k) = 0; 
                if ( (i < xmax) && (i > (xmax-5)) && (j < ymax) && (j > ymin))
                    *(img + i + IMG_WIDTH*j + IMG_WIDTH*IMG_HEIGHT*k) = 0; 
                if ( (j > ymin) && (j < (ymin+5)) && (i < xmax) && (i > xmin))
                    *(img + i + IMG_WIDTH*j + IMG_WIDTH*IMG_HEIGHT*k) = 0; 
                if ( (j < ymax) && (j > (ymax-5)) && (i < xmax) && (i > xmin))
                    *(img + i + IMG_WIDTH*j + IMG_WIDTH*IMG_HEIGHT*k) = 0; 
            }
        }
    }
}

void drawBoundingBoxOnImage(cv::Mat &image, double yMin, double xMin, double yMax, double xMax, double score, std::string label, bool scaled) {
    cv::Point tl, br;
    if (scaled) {
        tl = cv::Point((int) (xMin * image.cols), (int) (yMin * image.rows));
        br = cv::Point((int) (xMax * image.cols), (int) (yMax * image.rows));
    } else {
        tl = cv::Point((int) xMin, (int) yMin);
        br = cv::Point((int) xMax, (int) yMax);
    }
    cv::rectangle(image, tl, br, cv::Scalar(0, 0, 0, 255), 1);

    // Ceiling the score down to 3 decimals (weird!)
    float scoreRounded = floorf(score * 1000) / 1000;
    std::string scoreString = std::to_string(scoreRounded);
    //std::string scoreString = std::to_string(scoreRounded).substr(0, 5);
    std::string caption = label + " (" + scoreString + ")";

    // Adding caption of type "LABEL (X.XXX)" to the top-left corner of the bounding box
    int fontCoeff = 7;
    cv::Point brRect = cv::Point(tl.x + caption.length() * fontCoeff / 1.6, tl.y + fontCoeff);
    cv::rectangle(image, tl, brRect, cv::Scalar(0, 0, 0, 255), 0.01);
    cv::Point textCorner = cv::Point(tl.x, tl.y + fontCoeff * 0.9);
    cv::putText(image, caption, textCorner, cv::FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255, 255));
}
