#include <RgbImage.hpp>

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

RgbImage::RgbImage(uint32_t width, uint32_t height, uint32_t channels, off_t phy_addr) : __width(width), __height(height), __channels(channels) {
	__mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
	if ( __mem_fd == -1) 
		throw(std::runtime_error("Open /dev/mem Failed \n"));
	
	// phys_addr should be page-aligned
	__data.data = (uchar *)mmap(  NULL, 
																__getFootprint(), 
																PROT_READ | 
																PROT_WRITE, 
																MAP_SHARED, 
																__mem_fd, 
																phy_addr);
	if(__data.data == MAP_FAILED)
		throw(std::runtime_error("Open /dev/mem Failed \n"));
}

RgbImage::RgbImage(uint32_t width, uint32_t height, uint32_t channels) : __width(width), __height(height), __channels(channels) {
	switch (channels) {
	case 0:
		__data = cv::Mat(width, height, CV_8UC1, cv::Scalar(0));
		break;
	case 3:
		__data = cv::Mat(width, height, CV_8UC3, cv::Scalar(0, 0, 0));
		break;
	case 4:
		__data = cv::Mat(width, height, CV_8UC4, cv::Scalar(0, 0, 0, 0));
		break;
	default:
		throw(std::runtime_error("RgbImage not support this channel size \n"));
		break;
	}
}

RgbImage::~RgbImage() {
	munmap(__data.data, __getFootprint());
	close(__mem_fd);
}

cv::Mat RgbImage::getData() { return __data; }

RgbImage RgbImage::rgbaToGray() {
	RgbImage grayImage(__width, __height, 0);
	cvtColor(__data, grayImage.getData(), cv::COLOR_RGBA2GRAY); 
	return grayImage;
}

RgbImage RgbImage::rgbResize(uint32_t width, uint32_t height, uint32_t channels) {
	RgbImage resizedImage(__width, __height, channels);
  cv::Mat resized;
	resize(resizedImage.getData(), resized, cv::Size(width, height), cv::INTER_AREA);
	return resizedImage;
}

size_t RgbImage::__getFootprint() {	return (__width*__height*__channels); }