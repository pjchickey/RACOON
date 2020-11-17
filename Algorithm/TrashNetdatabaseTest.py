import numpy as np

import tensorflow as tf
assert tf.__version__.startswith('2')

from tflite_model_maker import configs
from tflite_model_maker import ExportFormat
from tflite_model_maker import image_classifier
from tflite_model_maker import ImageClassifierDataLoader
from tflite_model_maker import model_spec


image_path = r"..\Images-resized"

data = ImageClassifierDataLoader.from_folder(image_path)
train_data, validation_data = data.split(0.9)
test_data = ImageClassifierDataLoader.from_folder(r"C:\Users\sotoa\PycharmProjects\RACOON\test-folder")

model = image_classifier.create(train_data, model_spec=model_spec.efficientnet_lite0_spec, validation_data=validation_data)

loss, accuracy = model.evaluate(test_data)


#model.export(export_dir='.', tflite_filename='model_efficientnet_lite0.tflite')

print("loss", loss)
print("accuracy", accuracy)

#loss 0.7411657571792603
#accuracy 0.8695651888847351
