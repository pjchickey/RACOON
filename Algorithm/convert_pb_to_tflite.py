import tensorflow as tf


saved_model_dir = 'Images/saved_models/racoon/'

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir) # path to the SavedModel directory
tflite_model = converter.convert()

# Save the model.
with open('racoon01.tflite', 'wb') as f:
  f.write(tflite_model)
