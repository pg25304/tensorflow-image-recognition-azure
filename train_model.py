import tensorflow as tf
from tensorflow import keras

# Load the CIFAR-10 image dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Scale pixel values from 0-255 to 0-1
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Build the image-recognition neural network
model = keras.Sequential([
    keras.layers.Input(shape=(32, 32, 3)),
    keras.layers.Conv2D(32, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

# Prepare the model for training
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train the model
model.fit(
    x_train,
    y_train,
    epochs=5,
    validation_split=0.1
)

# Evaluate the model using unseen test images
test_loss, test_accuracy = model.evaluate(x_test, y_test)

print(f"\nTest accuracy: {test_accuracy:.4f}")

# Save the trained model
model.save("image_classifier.keras")
