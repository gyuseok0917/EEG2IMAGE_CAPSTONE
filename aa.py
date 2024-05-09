from io import BytesIO
from PIL import Image
from flask import Flask, send_file


class ImageGenProcess:
    def __init__(self, model = None):
        
        self.model = None
        
        self.app = Flask(__name__)
        self.add_routes()
        
        self.flask_runs()
        
    
    def generation_process(self):
        """
        EEG data get process
        """
        
        """
        Genration process
        """
        
        """
        Image Return
        """
        image = Image.open("tiger.jpg")
        return image
    
    
    def image_transfer(self):
        image = self.generation_process()
        
        image_bytes = BytesIO()
        image.save(image_bytes, "JPEG", quality = 70)
        image_bytes.seek(0)
        
        return send_file(image_bytes, mimetype = "image/jpeg", as_attachment=True, attachment_filename='filename.jpg')
        
    
    def add_routes(self):
        self.app.add_url_rule('/transfer', 'transfer', self.image_transfer, methods=['GET'])
        
    
    def flask_runs(self):
        self.app.run(host="0.0.0.0", port="5000", debug=True)


if __name__ == "__main__":
    process = ImageGenProcess()