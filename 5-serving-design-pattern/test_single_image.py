import tensorflow as tf
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    '--image_path',
    type=str,
    help="input single image"
)
args = parser.parse_args()
image_path = args.image_path

image = tf.keras.utils.load_img(image_path)
image = image.convert("L")
image = np.array(image) / 255.0
image = image.reshape(-1, 28, 28, 1)

model = tf.keras.models.load_model("mnist_model.h5")
predictions = model([image])
result = np.argmax(predictions[0])

print(f"예측한 값은: {result}입니다.")