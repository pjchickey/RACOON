import numpy as np
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from tflite_model_maker import ImageClassifierDataLoader
from RACOONdatabaseTest import test_data

thisdict = {0: "Aluminum", 1: "Cardboard-Boxes", 2: "Cardboard-Other", 3: "Glass", 4: "Other", 5: "Paper-Junk_Mail", 6: "Paper-Other", 7: "Plastic-Bottles", 8: "Plastic-Other", 9: "Plastic_Bags", 10: "Plasticware", 11: "Steel_and_Tin", 12: "Styrofoam"}
#dataset_labels = np.array([key.title() for key, value in thisdict])
dataset_labels = np.array(thisdict.values())
print(dataset_labels)

#image_path = r"C:\Users\sotoa\PycharmProjects\RACOON\Images-resized"
#data = ImageClassifierDataLoader.from_folder(image_path)
val_image_batch = test_data

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path=r"tflite_models\model_efficientnet_lite0.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("== Input details ==")
print("name:", input_details[0]['name'])
print("shape:", input_details[0]['shape'])
print("type:", input_details[0]['dtype'])

print("\n== Output details ==")
print("name:", output_details[0]['name'])
print("shape:", output_details[0]['shape'])
print("type:", output_details[0]['dtype'])


# Resize input and output tensors
interpreter.resize_tensor_input(input_details[0]['index'], (32, 224, 224, 3))
interpreter.resize_tensor_input(output_details[0]['index'], (32, 5))
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("\n== Input details ==")
print("name:", input_details[0]['name'])
print("shape:", input_details[0]['shape'])
print("type:", input_details[0]['dtype'])

print("\n== Output details ==")
print("name:", output_details[0]['name'])
print("shape:", output_details[0]['shape'])
print("type:", output_details[0]['dtype'])

#Invoke interpreter
interpreter.set_tensor(input_details[0]['index'], val_image_batch)

interpreter.invoke()

tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])
print("Prediction results shape:", tflite_model_predictions.shape)



tflite_pred_dataframe = pd.DataFrame(tflite_model_predictions)
tflite_pred_dataframe.columns = dataset_labels

print("TFLite prediction results for the first elements")
tflite_pred_dataframe.head()