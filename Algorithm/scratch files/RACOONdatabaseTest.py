import tensorflow as tf
assert tf.__version__.startswith('2')

from tflite_model_maker import configs
from tflite_model_maker import ExportFormat
from tflite_model_maker import image_classifier
from tflite_model_maker import ImageClassifierDataLoader
from tflite_model_maker import model_spec


image_path = r"../../Images-resized"

data = ImageClassifierDataLoader.from_folder(image_path)
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)

model = image_classifier.create(train_data, model_spec=model_spec.efficientnet_lite0_spec, validation_data=validation_data)

loss, accuracy = model.evaluate(test_data)

print("loss =", loss)
print("accuracy =", accuracy)

model.export(export_dir=r"../tflite_models", tflite_filename='model_efficientnet_lite0.tflite')


#loss = 1.2553505897521973
#accuracy = 0.699999988079071