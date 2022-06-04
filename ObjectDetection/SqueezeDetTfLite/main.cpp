#include "func.hpp"

#define DETECT_NUM 25

struct DetectResult {
	int label = -1;
	float score = 0;
	float ymin = 0.0;
	float xmin = 0.0;
	float ymax = 0.0;
	float xmax = 0.0;
};


int main(void) 
{
    // TfLite
    TfLiteModel* model;
    TfLiteInterpreterOptions* options;
    TfLiteInterpreter* interpreter;
    TfLiteTensor* model_input;
    const TfLiteTensor* model_output;
    TfLiteStatus invoke_status;
    const TfLiteTensor* m_output_locations;
    const TfLiteTensor* m_output_classes;
    const TfLiteTensor* m_output_scores;
    const TfLiteTensor* m_num_detections;
    const float* detection_locations;
    const float* detection_classes;
    const float* detection_scores; 
    int num_detections;
    int width ;
    int height;
    float max_prob=0;
    int detected=0;
    int index[DETECT_NUM];
    DetectResult* res = new DetectResult[DETECT_NUM];

    // OpenCV
    int mem_fd;
    void *img_read = NULL;
    void *img_write = NULL;
    cv::Mat img, img_cv, img_gray, img_blur;
    std::vector<cv::Mat> channels(3);
    int img_size;   

    // Measure time
    struct timespec begin, end; 
    int i;

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

    // Load Model
    model = TfLiteModelCreateFromFile(modelFileName);
    if (model == NULL){
        std::cout << "failed to load model" << std::endl;
        return -1;
    }
    options = TfLiteInterpreterOptionsCreate();
    TfLiteInterpreterOptionsSetNumThreads(options, 2);

    // Create Interpreter
    interpreter = TfLiteInterpreterCreate(model, options);
    if (interpreter == NULL){
        std::cout << "Failed to initiate the interpreter" << std::endl;
        return -1;
    }
    
    // Allocate Tensors
    if (TfLiteInterpreterAllocateTensors(interpreter) != kTfLiteOk){
        std::cout << "Failed to allocate tensor" << std::endl;
        return -1;
    }

    // Get Input Tensor 
    printf("Cantidad de entradas %d\n", TfLiteInterpreterGetInputTensorCount(interpreter));
    model_input = TfLiteInterpreterGetInputTensor(interpreter, 0);

    printf("model_input type %d\n", model_input->type);

    // Obtain a pointer to the output tensor
    printf("Cantidad de salidas %d\n", TfLiteInterpreterGetOutputTensorCount(interpreter));
	m_output_locations = TfLiteInterpreterGetOutputTensor(interpreter, 0);
	m_output_classes = TfLiteInterpreterGetOutputTensor(interpreter, 1);
	m_output_scores = TfLiteInterpreterGetOutputTensor(interpreter, 2);
	m_num_detections = TfLiteInterpreterGetOutputTensor(interpreter, 3);

    while(1){

        // Read mem address 
        memcpy(img.data, img_read, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);

        // Gray scale 1 channel
        //cvtColor(img, img, cv::COLOR_RGBA2GRAY);

        // Blur the image
        //GaussianBlur(img, img, std::Size(3,3), 0);

        // Edge detector
        //Canny(img,img,60,100);

        // Gray Scale 3 channels
        //cvtColor(img, img, cv::COLOR_GRAY2RGBA);

        // Le quito el cuarto canal (alfa)
        cvtColor(img, img_cv, cv::COLOR_RGBA2RGB);

        // Its not neccesary
        img_cv.convertTo(img_cv, CV_8UC3);
        
        // Write CNN input
        memcpy(model_input->data.uint8, img_cv.data, TfLiteTensorByteSize(model_input));

        // Start measuring time 
        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &begin);

        // Run the model on the spectrogram input and make sure it succeeds.
        invoke_status = TfLiteInterpreterInvoke(interpreter);
        if (invoke_status != kTfLiteOk) {
            std::cout << "Invoke failed" << std::endl;
            return -1;
        }

        // Stop measuring time and calculate the elapsed time
        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
        long seconds = end.tv_sec - begin.tv_sec;
        long nanoseconds = end.tv_nsec - begin.tv_nsec;
        double elapsed = seconds + nanoseconds*1e-9;
        printf("Time executing.. %f \n", elapsed);

        // Read CNN output
        float* detection_locations = m_output_locations->data.f;
        float* detection_classes = m_output_classes->data.f;
        float* detection_scores = m_output_scores->data.f;
        int num_detections = (int)*m_num_detections->data.f;
        
        //printf("num_detections %d \n", num_detections);
        //for (i=0;i<2500;i++)
        //    printf("%f ", detection_scores);

        width = img_cv.cols;
        height = img_cv.rows;

        for (int i = 0; i < num_detections && i < DETECT_NUM; ++i) {
            res[i].score = detection_scores[i];

            if(res[i].score > PROB_TRSH){
                index[detected] = i;
                detected++;
            }

/*             if (max < res[i].score){
                max = res[i].score;
                max_index = i;
            } */

            res[i].label = (int)detection_classes[i];
            res[i].ymin = detection_locations[i * 4] * height;
            res[i].xmin = detection_locations[i * 4 + 1] * width;
            res[i].ymax = detection_locations[i * 4 + 2] * height;
            res[i].xmax = detection_locations[i * 4 + 3] * width;
        }

        img.convertTo(img, CV_8UC4);
        //printf("max %f, max_index %d\n", max_prob, max_index);
        for(i=0;i<detected;i++){
            printf("max %f, max_index %d\n", res[i].score, i);
            drawBoundingBoxOnImage(img, res[i].ymin, res[i].xmin, res[i].ymax, res[i].xmax, res[i].score, "Test", false);
        }
        // Write time elapsed on image
        cv::Scalar font_Color(255, 255, 255, 255);
        cv::putText(img, std::to_string(elapsed), cv::Point(100,220), cv::FONT_HERSHEY_TRIPLEX, 0.5, font_Color, 1);

        // Write RAM
        memcpy(img_write, img.data, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);

        max_prob = 0;
        detected = 0;
    }

    // Dispose of the model and interpreter objects.
    TfLiteInterpreterDelete(interpreter);
    TfLiteInterpreterOptionsDelete(options);
    TfLiteModelDelete(model);
    
    return 0;
}