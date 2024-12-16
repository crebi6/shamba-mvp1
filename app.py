from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the .keras model
model = load_model("code/model/my_model.keras")

# Define classes (update this with your actual class names)
CLASS_NAMES = [
    "Blight",
    "Common Rust",
    "Gray Leaf Spot",
    "Maize Ear Rot",
    "Fall Armyworm",
    "Stem Borer",
    "Healthy Plant"
]

# Preprocess the image
def preprocess_image(image, target_size):
    image = image.resize(target_size)
    image = np.array(image) / 255.0  # Normalize the image
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        # Open the image
        image = Image.open(file.stream)
        processed_image = preprocess_image(image, target_size=(224, 224)) 
        predictions = model.predict(processed_image)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))

        return jsonify({
            "class": predicted_class,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
