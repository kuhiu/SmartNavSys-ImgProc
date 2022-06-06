import tensorflow as tf

saved_model_dir="./ssd_mobilenet_v2_fpnlite_320x320_1/"

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir) # path to the SavedModel directory
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
                                       tf.lite.OpsSet.TFLITE_BUILTINS]
#converter.inference_input_type = tf.uint8  # or tf.uint8
#converter.inference_output_type = tf.uint8  # or tf.uint8
tflite_model = converter.convert()

# Save the model.
with open('MyModel.tflite', 'wb') as f:
    f.write(tflite_model)