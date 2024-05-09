import json
import base64
import zlib
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
from PIL import Image
from flask import Flask, request, send_file


class Model:
    """
    Model for temporary testing
    """
    def __init__(self):
        pass
    
    def __call__(self, inputs):
        image = Image.open("image/tiger.jpg")
        return image


class ImageGenProcess:
    """
    Provides a process for receiving EEG data from a client, creating an image
    through a deep learning model, and transmitting it.
    
    Args:
        model: Using model
    """
    def __init__(self, model = None):
        
        self.model = model
        
        # Flask application
        self.app = Flask(__name__)
        
        # Method's router setting
        self.add_routes()
        
        # Flask app operation
        self.flask_runs()
        
        
    def get_eeg(self):
        """
        Receive EEG data from client
        """
        
        json_data = request.get_json()
        encoded_data = json_data['eeg_data'] # Encoded eeg data
        data_shape = json_data["shape"]      # EEG data's shape
        compressed_data = base64.b64decode(encoded_data) # Decode base64 format
        data_bytes = zlib.decompress(compressed_data) # Restore compressed data
        
        # Convert byte form to numpy matrix (reshape to size of original data)
        data_array = np.frombuffer(data_bytes, dtype=np.float32).reshape(data_shape)
        print(data_array.shape)
        
        return data_array
        
    
    def generation_process(self):
        """
        Generate EEG data received from client and create image using A.I.
        """
        
        eeg_data = self.get_eeg() # Get eeg data
        image = self.model(eeg_data) # Model operation

        return image
    
    
    def send_image(self):
        """
        Method for transmitting images generated from a deep learning model to the client
        """
        
        # Image Generation
        image = self.generation_process()
        
        # Save image in byte form
        image_bytes = BytesIO()
        image.save(image_bytes, "JPEG", quality = 70)
        image_bytes.seek(0)
        
        return send_file(image_bytes, mimetype = "image/jpeg", as_attachment=True, download_name = 'filename.jpg')
        
    
    def add_routes(self):
        """
        Specify the URL path to receive the client's request
        """
        self.app.add_url_rule('/transfer', 'transfer', self.send_image, methods=['POST'])
        
    
    def flask_runs(self):
        """
        Flask Application Operation
        """
        self.app.run(host="0.0.0.0", port="5000", debug=True)


if __name__ == "__main__":
    process = ImageGenProcess(model = Model())