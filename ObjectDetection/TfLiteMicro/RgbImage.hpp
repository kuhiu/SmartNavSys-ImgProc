#ifndef __RGBIMAGE_H__
#define __RGBIMAGE_H__

#include <cinttypes>
#include <opencv2/opencv.hpp>

class RgbImage {
public:
	/** RgbImage constructor */
	RgbImage(uint32_t width, uint32_t height, uint32_t channels, off_t phy_addr);
	/** Empty RgbImage constructor */
	RgbImage(uint32_t width, uint32_t height, uint32_t channels);
	/** RgbImage destructor */
	~RgbImage();
	/**
	 * @brief Get the Data 
	 * 
	 * @return cv::Mat 
	 */
	cv::Mat getData();
	/**
	 * @brief Transform rgba image to a gray image  
	 * 
	 * @param width 
	 * @param height 
	 * @param channels 
	 * @return RgbImage 
	 */
	RgbImage rgbaToGray();
	/**
	 * @brief Resize to specific width and height
	 * 
	 * @param width 
	 * @param height 
	 * @return RgbImage 
	 */
	RgbImage rgbResize(uint32_t width, uint32_t height, uint32_t channels);

private:
	/** Image data */
	cv::Mat __data;
	/** Image width */
	const uint32_t __width;
	/** Image height */
	const uint32_t __height;
	/** Image channels*/
	const uint32_t __channels;
	/** Memory file descriptor */
	int __mem_fd;
	/**
	 * @brief Get image footprint
	 * 
	 * @return size_t 
	 */
	size_t __getFootprint();
	
};

#endif // __RGBIMAGE_H__