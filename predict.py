import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

# CIFAR-10 class names
class_names = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

# Load the trained model
model = keras.models.load_model("image_classifier.keras")

# Load CIFAR-10 test images
(_, _), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Prepare one test image
image = x_test[1].astype("float32") / 255.0
image = np.expand_dims(image, axis=0)

# Make a prediction
prediction = model.predict(image)

predicted_class = np.argmax(prediction)
actual_class = y_test[1][0]

print("Predicted:", class_names[predicted_class])
print("Actual:", class_names[actual_class])
# Display the test image with prediction result
plt.imshow(x_test[1])
plt.title(
    f"Predicted: {class_names[predicted_class]} | "
    f"Actual: {class_names[actual_class]}"
)
plt.axis("off")
plt.show()