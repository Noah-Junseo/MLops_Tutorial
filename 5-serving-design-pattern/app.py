from io import BytesIO
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import tensorflow as tf
import uvicorn
import numpy as np
app = FastAPI()
def load_model():
    model_path = "mnist_model.h5"
    model = tf.keras.models.load_model(model_path)
    return model
def data_preprocessing(image):
    input_shape = model.layers[0].input_shape
    image = image.resize((input_shape[1], input_shape[2]))
    image = image.convert("L")
    image = np.array(image) / 255.0
    batch_image = np.array([image])  # (28, 28) to (1, 28, 28)
    return batch_image
@app.get("/")
def root_route():
    return {"error": "use POST /prediction instead of root route"}
@app.post("/prediction")
async def prediction_route(image: UploadFile = File(...)):
    contents = await image.read()
    pil_image = Image.open(BytesIO(contents))
    batch_image = data_preprocessing(pil_image)
    predictions = model(batch_image)
    result = np.argmax(predictions[0])
    return {f"예측한 값은: {result}입니다."}
if __name__ == "__main__":
    model = load_model()
    uvicorn.run(app, host='0.0.0.0', port=8079)
