import flask
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import numpy as np
import imutils
import urllib.request
import cv2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/predict": {"origins": "http://localhost:5000"}})

model = None
model_name = '4th_model.model'


@app.route('/')
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def index():
    return "AI is up and running."


@app.route('/model-name', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def get_model_name():
    return model_name


@app.route('/predict', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def process():
    req_data = request.get_json()

    input_word = req_data['inputWord']
    url = req_data['url']

    prediction_result = predict(input_word, url)

    return prediction_result


@app.route('/prediction-image', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def get_prediction_image():
    req_data = request.get_json()
    prediction_image_url = req_data['predictionImageUrl']

    return send_file(prediction_image_url, mimetype='image/png')


def get_colour(value):
    colour = (0, 0, 255)
    value = value * 100

    if value >= 70:
        colour = (0, 255, 0)
    elif value >= 40:
        colour = (0, 255, 255)
    elif value >= 10:
        colour = (0, 55, 200)
    else:
        colour = (0, 0, 255)

    return colour


def pre_process_image(image):
    image = cv2.resize(image, (28, 28))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image


def load_model_from(model_name):
    model = load_model(model_name)
    return model


def get_prediction_based_on_model(model, image):
    prediction = model.predict(image)[0]
    return prediction


def pretty_print_text(image, text, position, colour):
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, lineType=cv2.LINE_AA)
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, colour, 2, lineType=cv2.LINE_AA)


def get_image_from_word(word):
    image = cv2.imread('test/' + word + '.png')
    return image


def get_image_from_url(input_word, url):
    urllib.request.urlretrieve(url, 'tmp/' + input_word + '.png')
    print('Image downloaded!')
    image = cv2.imread('tmp/' + input_word + '.png')
    return image


def get_pretty_labels_from_prediction(prediction):
    animal_label = "{}: {:.2f}%".format('Animal', prediction[0] * 100)
    mineral_label = "{}: {:.2f}%".format('Mineral', prediction[1] * 100)
    vegetable_label = "{}: {:.2f}%".format('Vegetable', prediction[2] * 100)

    return [animal_label, mineral_label, vegetable_label]


def predict(input_word, url):
    # original_image = get_image_from_word(input_word)
    original_image = get_image_from_url(input_word, url)

    pre_processed_image = pre_process_image(original_image)
    prediction = get_prediction_based_on_model(model, pre_processed_image)

    pretty_labels = get_pretty_labels_from_prediction(prediction)
    output = imutils.resize(original_image, width=400)

    y_text_position = 25

    for i, label in enumerate(pretty_labels):
        colour = get_colour(prediction[i])
        pretty_print_text(output, label, (2, y_text_position), colour)
        y_text_position = y_text_position + 20

    pretty_print_text(output, 'Word: ' + input_word, (2, 200), (255, 153, 204))

    prediction_image_url = 'static/predictions/' + input_word + '.png'
    cv2.imwrite(prediction_image_url, output)

    prediction = [str(prediction[0]), ',', str(prediction[1]), ',', str(prediction[2])]

    return {
        'prediction': ''.join(prediction),
        'predictionImageUrl': prediction_image_url
    }
    # cv2.imshow('Prediction for: ' + word, output)
    #
    # while True:
    #     key = cv2.waitKey(0)
    #
    #     if key == 27:  # ESC Key
    #         break


# def main():
#     word = 'broccoli'
#     model = load_model_from('models/4th_model.model')
#     original_image = get_image_from_word(word)
#
#     pre_processed_image = pre_process_image(original_image)
#     prediction = get_prediction_based_on_model(model, pre_processed_image)
#
#     pretty_labels = get_pretty_labels_from_prediction(prediction)
#     output = imutils.resize(original_image, width=400)
#
#     y_text_position = 25
#
#     for i, label in enumerate(pretty_labels):
#         colour = get_colour(prediction[i])
#         pretty_print_text(output, label, (2, y_text_position), colour)
#         y_text_position = y_text_position + 20
#
#     pretty_print_text(output, 'Word: ' + word, (2, 200), (255, 153, 204))
#
#     cv2.imwrite('predictions/' + word + '.png', output)
#     cv2.imshow('Prediction for: ' + word, output)
#
#     while True:
#         key = cv2.waitKey(0)
#
#         if key == 27:  # ESC Key
#             break


if __name__ == '__main__':
    model = load_model_from('static/models/' + model_name)
    app.run()
    # main()

# Args
# ap = argparse.ArgumentParser()
# ap.add_argument("-m", "--model", required=True,
# 	help="path to trained model model")
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# args = vars(ap.parse_args())
#
# # load the image
# image = cv2.imread(args["image"])
# orig = image.copy()
#
# # Image Pre-processing
# image = cv2.resize(image, (28, 28))
# image = image.astype("float") / 255.0
# image = img_to_array(image)
# image = np.expand_dims(image, axis=0)
#
# # Load CNN
# print("[INFO] loading network...")
# model = load_model(args["model"])
#
# # Get the predictions
# result = model.predict(image)[0]
#
# animal = result[0]
# mineral = result[1]
# vegetable = result[2]
#
# animal_label = "{}: {:.2f}%".format('Animal', animal * 100)
# mineral_label = "{}: {:.2f}%".format('Mineral', mineral * 100)
# vegetable_label = "{}: {:.2f}%".format('Vegetable', vegetable * 100)
#
# animal_label_colour = get_colour(animal)
# mineral_label_colour = get_colour(mineral)
# vegetable_label_colour = get_colour(vegetable)
#
# print(animal_label_colour)
# print(mineral_label_colour)
# print(vegetable_label_colour)
#
# output = imutils.resize(orig, width=400)
#
# cv2.putText(output, animal_label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, lineType=cv2.LINE_AA)
# cv2.putText(output, animal_label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, animal_label_colour, 2, lineType=cv2.LINE_AA)
#
# cv2.putText(output, mineral_label, (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, lineType=cv2.LINE_AA)
# cv2.putText(output, mineral_label, (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, mineral_label_colour, 2, lineType=cv2.LINE_AA)
#
# cv2.putText(output, vegetable_label, (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, lineType=cv2.LINE_AA)
# cv2.putText(output, vegetable_label, (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, vegetable_label_colour, 2, lineType=cv2.LINE_AA)
#
# cv2.putText(output, 'Word: meat loaf', (10, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, lineType=cv2.LINE_AA)
# cv2.putText(output, 'Word: meat loaf', (10, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.6, vegetable_label_colour, 2, lineType=cv2.LINE_AA)
#
# cv2.imshow("Prediction", output)
#
# img_name = args["image"].split('/')[1]
# print(img_name)
# cv2.imwrite('predictions/' + img_name, output)
#
# while True:
# 	key = cv2.waitKey(0)
#
# 	if key == 27:  # ESC Key
# 		break
