from flask import Flask, request, jsonify
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-printed')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-printed')

app = Flask(__name__)

@app.route('/')
def index():
    return "Linux OCR API made by upio"

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return "No image found in the request"
    
    image_file = request.files['image']
    image = Image.open(image_file)
    
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return jsonify({'text': generated_text})

@app.route('/stop', methods=['POST'])
def stop():
    print("Stopping...")
    os._exit(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)