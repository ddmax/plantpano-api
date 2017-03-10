import logging
import os

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request, redirect, flash
from flask.helpers import make_response
from werkzeug.utils import secure_filename

# Flask confs
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif', 'tiff', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '{ddmax}'
app.config['DEBUG'] = True

# Tensorflow confs
NUM_CLASSES = 5
NUM_TOP_CLASSES = 5
DATA_DIRNAME = os.path.join(app.root_path, 'data')

# Response codes and messages
CODE_CLASSIFY_SUCCESS = 0
MESSAGE_CLASSSIFY_SUCCESS = 'success'


def convolutional(input):
    return input


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PlantClassifier:
    default_args = {
        'model_graph_def_file': os.path.join(DATA_DIRNAME, 'model.pb'),
        'class_labels_file': os.path.join(DATA_DIRNAME, 'labels.txt')
    }
    for k, v in default_args.items():
        if not os.path.exists(v):
            raise Exception("File {} not found at {}".format(k, v))

    def __init__(self, model_graph_def_file, class_labels_file):
        logging.info('Loading model data and labels...')

        # Read model
        self.graph = self.load_graph(model_graph_def_file)
        # Read labels
        self.labels = self.load_labels(class_labels_file)

    def load_graph(self, model_graph_def_file):
        with tf.gfile.FastGFile(model_graph_def_file, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name='')
        return graph

    def load_labels(self, class_labels_file):
        labels_file = open(class_labels_file)
        lines = labels_file.read().splitlines()
        return [str(w) for w in lines]

    def classify_image(self, image, from_file=False):
        result = dict()

        image_data = tf.gfile.FastGFile(image, 'rb').read() if from_file \
            else tf.gfile.FastGFile(image, 'rb')

        with tf.Session(graph=self.graph) as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            top_k = predictions.argsort()[-5:][::-1]

            for node_id in top_k:
                plant_name = self.labels[node_id]
                score = format(predictions[node_id], '.4f')
                result[plant_name] = score

            return result


@app.route('/api/image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # Save image file
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)

            # Start classify image
            ret = app.classifier.classify_image(file_path, from_file=True)
            return make_response(jsonify(
                code=CODE_CLASSIFY_SUCCESS,
                message=MESSAGE_CLASSSIFY_SUCCESS,
                result=ret),
                200
            )

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/', methods=['GET'])
def main():
    return 'Hello PlantPano!'


def setup_app():
    app.classifier = PlantClassifier(**PlantClassifier.default_args)
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    setup_app()
