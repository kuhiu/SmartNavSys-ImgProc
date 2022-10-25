#include <PersonDetector.hpp>

#define FRAMEBUFFER_READ_OFFSET 0x01000000  // phy image offset

int main() {
  /** Image width */
  const int width = 96;
  /** Image height */
  const int height = 96;
  /** Image channel */
  const int channels = 1;

  /** PersonDetector */
  PersonDetector person_detector;

  /** Phy RgbImage */
  RgbImage rgba_image(320, 240, 4, (off_t)FRAMEBUFFER_READ_OFFSET);

  /** 320x240x4 rgba image -> 320x240x1 gray image */
  RgbImage gray_image = rgba_image.rgbaToGray();

  /** 320x240x1 -> 96x96x1 */
  RgbImage resized_image = rgba_image.rgbResize(width, height, channels);

  /** Run Person detector */
  RecognitionResult recognition_result = person_detector.run(resized_image);

  /** Print results */
  std::cout << "person = " << recognition_result.recognition_score << "no person" <<
  recognition_result.no_recognition_score << std::endl;

  return 0;
}