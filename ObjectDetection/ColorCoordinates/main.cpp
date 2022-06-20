#include "main.hpp"

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

int save_cX(struct sembuf *sb, int semid, FILE *fdd_State, int cX)
{
    ssize_t loffset, lread;
    char * line = NULL;
    size_t len = 0;  
    int lineNro;
    char aux[50];

    // Tomo el recurso
    sb->sem_op = -1;         
    if (semop(semid, sb, 1) == -1) {          
        perror("semop");
        exit(1);
    }

    /* Busco a lo largo del archivo "Sensores, rightSensor =" */
    lineNro = 0;
    loffset = 0;
    fseek(fdd_State, 0, SEEK_SET);
    while ( (lread=getline(&line, &len, fdd_State )) != -1)
    {
        lineNro++;
        loffset = loffset + lread;
        //printf("lineNro: %d \n", lineNro);
        //printf("line %s \n", line); 
        switch (sscanf(line, "ImgProc, Direccion = %s\n", aux ))
        {
            case EOF:       // Error
                perror("sscanf");
                exit(1);
                break;
            case 0:         // No encontro
                //printf("No se encontro la linea: Sensores, rightSensor \n");
                break;
            default:        // Encontro
                //printf("La linea es la nro: %d, offset: %d \n", lineNro, loffset); 
                //printf("line %s \n", line); 
                sprintf(line, "ImgProc, Direccion = %03d", cX);
                fseek(fdd_State, (loffset-lread), SEEK_SET);
                if ( ( fwrite(line, sizeof(char), strlen(line), fdd_State)) != strlen(line))
                {
                    printf("Error escribiendo\n");
                    return -1;
                }
                fseek(fdd_State, (loffset), SEEK_SET);
                break;
        }
    } 
    // Libero el recurso
    sb->sem_op = 1;          
    if (semop(semid, sb, 1) == -1) {
        perror("semop");
        exit(1);
    }
    free(line); 
    return 0;
}


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

    // Semaforo 
    key_t key;              
    int semid, fdp;
    struct sembuf sb;

    sb.sem_num = 0;
    sb.sem_op = -1; /* set to allocate resource */
    sb.sem_flg = SEM_UNDO;

    /* state file */
    FILE* fdd_State = NULL;

    // Measure time
    struct timespec begin, end; 

    int largest_area=0, area_is_zero=1;
    int largest_contour_index=0;

    int cX, cY;
    cv::Moments M;

    mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
    if ( mem_fd == -1)
    {
        printf("Open /dev/mem Failed\n");
        return -1;
    }

    // Inicializa el semaforo
    if((fdp=open("SemFile", O_RDONLY | O_CREAT, 0777))==-1){
        perror(" Open");
        exit(1);
    }
    if((key = ftok("SemFile", 'E'))==-1){
        perror(" ftok ");
        close(fdp);
        exit(1);
    }
    // Configura el semaforo
    if ((semid = initsem(key, 1)) == -1) {     
        perror("initsem");
        close(fdp);
        exit(1);
    }

    // Abro state.txt
    if ( (fdd_State = fopen("state.txt", "r+")) == NULL){
        printf("Error abriendo state.txt\n");
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

        // Get HSV image
        cv::cvtColor(img, img_bgr, cv::COLOR_RGBA2BGR);
        cv::cvtColor(img_bgr, img_hsv, cv::COLOR_BGR2HSV);

        // Mask
        cv::inRange(img_hsv, lower_green, uper_green, green_mask);

        // Find Contours
        cv::findContours(green_mask, green_contours, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);

        for( size_t i = 0; i< green_contours.size(); i++ ){ // iterate through each contour.
            double area = cv::contourArea( green_contours[i] );  //  Find the area of contour

            if( area > largest_area ){
                largest_area = area;
                largest_contour_index = i;               //Store the index of largest contour
                area_is_zero = 0;
                //bounding_rect = cv::boundingRect( green_contours[i] ); // Find the bounding rectangle for biggest contour
            }
        }

        if(!area_is_zero){
            // Largest contour
            largest_contour = green_contours[largest_contour_index];

            // Draw largest contour
            cv::drawContours(img, green_contours, largest_contour_index, cv::Scalar(0,0,0,255), 2);

            // Center of the contour
            M = cv::moments(largest_contour);
            cX = int(M.m10 / M.m00);
            cY = int(M.m01 / M.m00);

            DEBUG_PRINT(("cX: %d\n", cX));
            // Draw center of area
            cv::circle(img, cv::Point(cX, cY), 7, (255, 255, 255, 255), -1);

            // Stop measuring time and calculate the elapsed time
            clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
            long seconds = end.tv_sec - begin.tv_sec;
            long nanoseconds = end.tv_nsec - begin.tv_nsec;
            double elapsed = seconds + nanoseconds*1e-9;

            // Write time elapsed on image
            cv::putText(img, std::to_string(elapsed), cv::Point(100,220), cv::FONT_HERSHEY_TRIPLEX, 0.5, font_Color, 1);
        }
        else
            cX = -1;

        // Save cX in state
        save_cX( &sb, semid, fdd_State, cX);

        // Write mem address 
        memcpy(img_write, img.data, IMG_HEIGHT*IMG_WIDTH*IMG_CHANNEL);

        largest_area = 0;
        area_is_zero = 1;
    }

    return 0;
}