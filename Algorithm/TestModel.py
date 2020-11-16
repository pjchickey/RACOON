import numpy as np

import tensorflow as tf
assert tf.__version__.startswith('2')

from tflite_model_maker import configs
from tflite_model_maker import ExportFormat
from tflite_model_maker import image_classifier
from tflite_model_maker import ImageClassifierDataLoader
from tflite_model_maker import model_spec
from PIL import Image

thisdict = {0: "cardboard", 1: "glass", 2: "metal", 3: "paper", 4: "plastic", 5: "trash"}
# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("input details", input_details)
print("output details", output_details)

# Test the model on input data.
input_shape = input_details[0]['shape']


img = Image.open(r"C:\Users\sotoa\PycharmProjects\RACOON\Images-resized\Paper-Junk_Mail\bidenmailflyer0--20.png")
img = np.array(img, dtype=np.float32)
print("shape =", img.shape)
img = img[:, :, :3]
#img = np.array(img, dtype=np.float32)
print("shape =", img.shape)
img = np.expand_dims(img, axis=0)
print("shape =", img.shape)
#img = np.reshape(img, (1, 224, 224, 3))
#print("shape =", img.shape)



input_data = img

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
print('output data =', output_data)
print("category =", thisdict[np.argmax(output_data)])
print("index =", np.argmax(output_data))