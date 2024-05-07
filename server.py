from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Load your TensorFlow model
model = tf.keras.models.load_model('C:\\Users\\surfc\\IdeaProjects\\FishID\\my_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if request contains file data
        if 'uri' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        # Get file data from the request
        image_uri = request.files['uri']
        
        # Save the image to a temporary file
        temp_file = 'temp_image.jpg'
        image_uri.save(temp_file)
        
        # Preprocess input data
        processed_data = preprocess(temp_file)

        # Perform inference
        predictions = model.predict(processed_data)

        # Post-process predictions if necessary
        processed_predictions = postprocess(predictions)

        # Return predictions as JSON response
        return jsonify({'predictions': processed_predictions})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def preprocess(image_path):
    # Load the image
    img = image.load_img(image_path, target_size=(150, 150))
    # Convert image to numpy array
    img_array = image.img_to_array(img)
    # Expand dimensions to match model input shape
    processed_data = np.expand_dims(img_array, axis=0)
    # Normalize pixel values
    processed_data /= 255.0
    return processed_data

def postprocess(predictions):
    return predictions.tolist()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
