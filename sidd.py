from flask import Flask, request, render_template
import numpy as np
import tensorflow as tf
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image

app = Flask(__name__, template_folder ="templates")
model = tf.keras.models.load_model("brain_tumor_model.h5")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to predict tumor
def predict_tumor(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return "Tumor Detected" if prediction[0][0] > 0.5 else "No Tumor"

# Route for homepage
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            print(filepath)

            result = predict_tumor(filepath)
            return render_template("tumor.html", result=result, img_path=filepath)
    return render_template("tumor.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
