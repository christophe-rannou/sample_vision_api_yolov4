from flask import Flask, request, make_response
from werkzeug.exceptions import BadRequest
import cv2
import onnxruntime as rt
from inference import infer

# Create flask app
app = Flask(__name__)

# Init ONNX runtime session
ort_session = rt.InferenceSession('../resources/yolov4.onnx')


def is_picture(filename):
    image_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in image_extensions


def file_extension(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return f'.{ext}'


@app.route('/', methods=['POST'])
def annotate():
    file = extract_image(request)
    if file and is_picture(file.filename):
        # The image file seems valid! Detect faces and return the result.
        image = infer(file, ort_session)
        _, buffer = cv2.imencode(file_extension(file.filename), image)
        return make_response(buffer.tobytes())
    else:
        raise BadRequest("Given file is invalid!")


def extract_image(request):
    # Check if a valid image file was uploaded
    if 'file' not in request.files:
        raise BadRequest("Missing file parameter!")

    file = request.files['file']
    if file.filename == '':
        raise BadRequest("Given file is invalid")

    return file


if __name__ == "__main__":
    # Start app
    print("Starting WebServer...")
    app.run(host='0.0.0.0', port=8080, debug=False)
