# Get photo
#curl https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/lite/examples/label_image/testdata/grace_hopper.bmp > /tmp/grace_hopper.bmp
# Get model
#curl https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_02_22/mobilenet_v1_1.0_224.tgz | tar xzv -C /tmp
# Get labels
#curl https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_1.0_224_frozen.tgz  | tar xzv -C /tmp  mobilenet_v1_1.0_224/labels.txt

#mv /tmp/mobilenet_v1_1.0_224/labels.txt /tmp/

##python3 label_image.py \
#  --model_file /tmp/mobilenet_v1_1.0_224.tflite \
##  --label_file /tmp/labels.txt \
# --image /tmp/grace_hopper.bmp