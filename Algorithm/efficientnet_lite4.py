import numpy as np

import tensorflow as tf
assert tf.__version__.startswith('2')

from tflite_model_maker import configs
from tflite_model_maker import ExportFormat
from tflite_model_maker import image_classifier
from tflite_model_maker import ImageClassifierDataLoader
from tflite_model_maker import model_spec

import matplotlib.pyplot as plt

image_path = r"C:\Users\sotoa\PycharmProjects\pythonProject1\trashnet\data\dataset-resized"

data = ImageClassifierDataLoader.from_folder(image_path)

train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)

model = image_classifier.create(train_data, model_spec=model_spec.efficientnet_lite4_spec, validation_data=validation_data)



loss, accuracy = model.evaluate(test_data)

print("model", model.summary())
print("loss", loss)
print("accuracy", accuracy)

#model.export(export_dir='.', tflite_filename='model_efficientnet_lite4.tflite')

#loss 0.8085951209068298
#accuracy 0.8102766871452332