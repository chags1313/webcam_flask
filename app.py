from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Dummy function for image processing (replace with your actual image processing logic)
def process_image(image_stream):
    try:
        # Convert the image stream to a NumPy array
        image = cv2.imdecode(np.frombuffer(image_stream, np.uint8), -1)

        # Your image processing logic here
        # For demonstration purposes, we'll apply a simple grayscale filter
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Encode the processed image back to a stream
        _, processed_image = cv2.imencode('.jpg', gray_image)

        return processed_image.tobytes(), []

    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    return render_template('cam.html')

@app.route('/process_image', methods=['POST'])
def process_image_route():
    try:
        image_stream = request.files['image'].read()
        image_data, keypoints = process_image(image_stream)
        if image_data:
            response_data = {
                'image': image_data.decode('latin1'),  # Convert bytes to string
                'keypoints': keypoints
            }
            return jsonify(response_data)
        else:
            return jsonify({'error': 'Image processing failed'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Use the provided $PORT variable by Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

