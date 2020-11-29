import numpy as np
import tensorflow as tf
import glob
from PIL import Image

thisdict = {0: "cardboard", 1: "glass", 2: "metal", 3: "paper", 4: "plastic", 5: "trash"}
# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path=r"tflite_models\model_efficientnet_lite0.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("input details", input_details)
print("output details", output_details)

# Test the model on input data.
image_list = []
mylist =[]
for filename in glob.glob(r'C:\Users\sotoa\PycharmProjects\RACOON\trashnet\data\dataset-resized\metal\*.jpg'):
    im=Image.open(filename)
    image_list.append(im)
    mylist.append(filename)

counter = 0

for pic in image_list:
    print("2")
    print("type1", type(pic))
    pic = np.array(pic, dtype=np.float32)
    print("type2", pic.dtype)
    pic = pic[:, :, :3]
    print("type3", pic.dtype)
    image_list[counter] = np.expand_dims(pic, axis=0)
    print("type4", pic.dtype)
    counter += 1
    print("shape =", pic.shape)
#print("first image", type(image_list[3]), image_list[3].dtype)

input_data = image_list
mydict = {}
mydict2 = {}

for i in range(len(input_data)):
    interpreter.set_tensor(input_details[0]['index'], input_data[i])
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    mydict[mylist[i]] = thisdict[np.argmax(output)]
    mydict2[mylist[i]] = np.argmax(output)
print("dict =", mydict.values())
