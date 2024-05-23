import time
import json
import base64
import zlib
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
from glob import glob
from PIL import Image
from flask import Flask, request, send_file, jsonify


class Model:
    """
    Model for temporary testing
    """
    def __init__(self):
        pass
    
    def __call__(self, inputs):
        image = []
        
        for path in glob("image/*.jpg"):
            image.append(Image.open(path))
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
        
        self.eeg_data = None
        
        
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
        data_array = np.frombuffer(data_bytes, dtype=np.float64).reshape(data_shape)
        
        print(f"Get EEG data: {data_array.shape}")
        print(f"Get Number: {json_data['number']}")
        
        return data_array
        
    
    def generation_process(self):
        """
        Generate EEG data received from client and create image using A.I.
        """
        
        eeg_data = self.get_eeg() # Get eeg data
        image = self.model(eeg_data) # Model operation
        
        self.eeg_data = eeg_data

        return eeg_data, image
    
    
    def send_image(self):
        """
        Method for transmitting images generated from a deep learning model to the client
        """
        
        # Image Generation
        eeg_data, image = self.generation_process()
        
        eeg_encoded = convert_byte_ee(eeg_data)        
        image_byte = [self.convert_byte_image(img) for img in image]
        
        return jsonify({"eeg_data": eeg_encoded, "images": image_byte, "shape": eeg_data.shape})
    
    
    def send_select_ch_eeg(self):
        
        json_data = request.get_json()
        n_ch = json_data['n_ch']
        
        select_ch_eeg = self.eeg_data[:, :n_ch]
        return jsonify({"eeg_data": select_ch_eeg, "shape": select_ch_eeg.shape})
        
        
    def convert_byte_eeg(self, eeg_data):
        eeg_bytes = eeg_data.tobytes()
        eeg_compressed = zlib.compress(eeg_bytes)
        eeg_encoded = base64.b64encode(eeg_compressed).decode('utf-8')
        return eeg_encoded     
    
    
    def convert_byte_image(self, image):
        image_bytes = BytesIO()
        image.save(image_bytes, "JPEG", quality = 70)
        image_bytes.seek(0)
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
        return image_base64
        
    
    def add_routes(self):
        """
        Specify the URL path to receive the client's request
        """
        self.app.add_url_rule('/transfer', 'transfer', self.send_image, methods=['POST'])
        self.app.add_url_rule('/select-ch', 'select-ch', self.send_select_ch_eeg, methods=['POST'])
        
    
    def flask_runs(self):
        """
        Flask Application Operation
        """
        self.app.run(host="0.0.0.0", port="5000", debug=True)


if __name__ == "__main__":
    process = ImageGenProcess(model = Model())
