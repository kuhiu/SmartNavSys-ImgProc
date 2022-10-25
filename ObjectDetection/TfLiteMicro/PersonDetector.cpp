#include <PersonDetector.hpp>

#include "./model/person_detect_model_data.h"

#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/system_setup.h"

#define DEBUG_PERSON_DETECTION 1
#if DEBUG_PERSON_DETECTION
#define APP_DEBUG(fmt, arg...) printf("%s()%d - ", fmt, __func__, __LINE__, ##arg)
#else
#define APP_DEBUG(fmt, arg...)
#endif

PersonDetector::PersonDetector() {
  APP_DEBUG("Entre al constructor de PersonDetector \n");
  tflite::InitializeTarget();

  APP_DEBUG("Map de model \n");
  // Map the model into a usable data structure. 
  __model = std::make_unique<tflite::Model> (tflite::GetModel(g_person_detect_model_data));
  if (__model->version() != TFLITE_SCHEMA_VERSION) {
    std::ostringstream err;
    err << "Model provided is schema version " << __model->version() << " not equal to supported version " << TFLITE_SCHEMA_VERSION;
    throw(std::runtime_error(err.str()));
  }

  APP_DEBUG("Pull the operation needed \n");
  // Pull in only the operation implementations we need or use the AllOpsResolver.
  // tflite::AllOpsResolver resolver;
  tflite::MicroMutableOpResolver<5> micro_op_resolver;
  micro_op_resolver.AddAveragePool2D(tflite::Register_AVERAGE_POOL_2D_INT8());
  micro_op_resolver.AddConv2D(tflite::Register_CONV_2D_INT8());
  micro_op_resolver.AddDepthwiseConv2D(tflite::Register_DEPTHWISE_CONV_2D_INT8());
  micro_op_resolver.AddReshape();
  micro_op_resolver.AddSoftmax(tflite::Register_SOFTMAX_INT8());

  APP_DEBUG("Build an interpreter \n");
  // Build an interpreter to run the model with.
  __interpreter = std::make_unique<tflite::MicroInterpreter> (  __model.get(), 
                                                                micro_op_resolver, 
                                                                __tensor_arena, 
                                                                __k_tensor_arena_size);

  // Allocate memory from the tensor_arena for the model's tensors.
  TfLiteStatus allocate_status = __interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) 
    throw(std::runtime_error("AllocateTensors() failed\n"));

  // Get information about the memory area to use for the model's input.
  __input = std::make_unique<TfLiteTensor> (__interpreter->input(0));
}

RecognitionResult PersonDetector::run(const RgbImage image) {
  // Run the model on this input and make sure it succeeds.
  if (__interpreter->Invoke() != kTfLiteOk) 
    throw(std::runtime_error("Invoke failed \n"));

  TfLiteTensor* output = __interpreter->output(0);

  // Process the inference results.
  RecognitionResult recognition_result;
  recognition_result.recognition_score = output->data.uint8[__k_person_index];
  recognition_result.no_recognition_score = output->data.uint8[__k_not_person_index]; 
  
  return recognition_result;
}