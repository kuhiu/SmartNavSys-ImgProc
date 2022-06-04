# Model link to download 
https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/default/1

# Step 1: Export TFLite inference graph

python3.6 object_detection/export_tflite_graph_tf2.py --pipeline_config_path ../../ssd_mobilenet_v2_320x320_coco17_tpu-8/pipeline.config --trained_checkpoint_dir ../../ssd_mobilenet_v2_320x320_coco17_tpu-8/checkpoint/ --output_directory ../../ssd_mobilenet_v2_320x320_coco17_tpu-8

# Step 2: Convert to TFLite

tflite_convert --saved_model_dir=./saved_model --output_file=./mobilenet.tflite