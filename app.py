import io
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from tensorflow import keras

app = FastAPI(title="TensorFlow Image Recognition API")

# CIFAR-10 class names
class_names = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

# Load the trained model once when the API starts
model = keras.models.load_model("image_classifier.keras")


@app.get("/")
def home():
    return {"message": "TensorFlow Image Recognition API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    # CIFAR-10 model expects 32x32 RGB images
    image = image.resize((32, 32))
    image_array = np.array(image).astype("float32") / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Make prediction
    prediction = model.predict(image_array, verbose=0)
    predicted_class = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return {
        "prediction": class_names[predicted_class],
        "confidence": round(confidence, 4)
    }