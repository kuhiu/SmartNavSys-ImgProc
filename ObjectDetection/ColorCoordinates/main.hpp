// C++ program for the above approach
#include <iostream>
#include <numeric>
#include <opencv2/opencv.hpp>
#include <sys/mman.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <cerrno>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <unistd.h>
#include <sstream>

#define MAX_RETRIES                10
#define FRAMEBUFFER_READ_OFFSET   0x01000000  // Image ram position
#define FRAMEBUFFER_WRITE_OFFSET  0x02000000  // Image ram position
#define IMG_WIDTH                 320   // Image size
#define IMG_HEIGHT                240
#define IMG_CHANNEL                 4

//#define DEBUG            1

#ifdef DEBUG
# define DEBUG_PRINT(x) printf x
#else
# define DEBUG_PRINT(x) 
#endif


// Semaforo
union semun {
    int val;
    struct semid_ds *buf;
    ushort *array;
};

int initsem(key_t key, int nsems);