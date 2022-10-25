#ifndef __PERSONDETECTION_H__
#define __PERSONDETECTION_H__

#include <RecognitionResult.hpp>
#include <RgbImage.hpp>

#include "tensorflow/lite/micro/micro_interpreter.h"

/* In order to use optimized tensorflow lite kernels, a signed int8_t quantized
model is preferred over the legacy unsigned model format. This means that
throughout this project, input images must be converted from unisgned to
signed format. The easiest and quickest way to convert from unsigned to
signed 8-bit integers is to subtract 128 from the unsigned value to get a
signed value. */

class PersonDetector {
public:
	/** PersonDetector constructor */
	PersonDetector();
	/** PersonDetector destructor*/
	~PersonDetector() = default;
	/** PersonDetector initializer */
	void setup();
	/**
	 * @brief Run person detection 
	 * 
	 * @param image 
	 * @return * Run 
	 */
	RecognitionResult run(const RgbImage image);

private:
	/** Size of an area of memory to use for input, output, and intermediate arrays */
	static const int __k_tensor_arena_size = 136 * 1024;
	/** Person index */
	const int __k_person_index = 1;
	/** No person index */
	const int __k_not_person_index = 0;
	/** Area of memory to use for input, output, and intermediate arrays */
	uint8_t __tensor_arena[__k_tensor_arena_size];
	/** Tflite model */
	std::unique_ptr<tflite::Model> __model;
	/** Tflite interpreter */
	std::unique_ptr<tflite::MicroInterpreter> __interpreter;
	/** Tflite input */
	std::unique_ptr<TfLiteTensor> __input;


};


#endif // __PERSONDETECTION_H__