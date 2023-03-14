from flask import Flask
from flask_restful import Api, Resource, reqparse
import cv2
import PIL

from .functions_for_images.opencv_cleaner import clean_scaner


app = Flask(__name__)
api = Api()


parser = reqparse.RequestParser()
parser.add_argument("name", type=str)
parser.add_argument("videos", type=int)


class Main(Resource):
    def get(self, course_id):
        return {'name': f'success {course_id}'}

    def post(self, userid):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('photo', type=bytes)
            img = parser.parse_args()['photo']
            autoencoded_img = get_autoencoded_image(img)

            autoencoded_image_encode = cv2.imencode('.png', autoencoded_img)[1]
            autoencode_encode = np.array(autoencoded_image_encode)
            autoencode_byte_encode = autoencode_encode.tobytes()
        except TypeError:
            return {"answer":"error with your picture formate"}

        cleaned_opencv_image = clean_scaner(img)
        cleaned_opencv_image_encode = cv2.imencode('.png', cleaned_opencv_image)[1]
        cleaned_opencv_data_encode = np.array(cleaned_opencv_image_encode)
        cleaned_opencv_byte_encode = cleaned_opencv_data_encode.tobytes()

        pil_img = Image.fromarray(autoencoded_img)
        pil_img = pil_img.convert('RGB')
        text_from_image = pytesseract.image_to_string(pil_img, lang='eng')
        return {"autoencoder_cleaner": base64.b64encode(autoencode_byte_encode), "open_cv_cleaner" : base64.b64encode(cleaned_opencv_byte_encode), "text" : text_from_image}


api.add_resource(Main, "/api/denoise/")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
