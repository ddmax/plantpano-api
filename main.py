import logging

from flask import Flask, jsonify, request, make_response, redirect, flash
from werkzeug.utils import secure_filename
import os
import tensorflow as tf


app = Flask(__name__)

# Flask confs
DATA_DIRNAME = os.path.join(app.root_path, 'data/')
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads/')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif', 'tiff', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = '{ddmax}'
app.config['DEBUG'] = True


def convolutional(input):
    return input


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PlantClassifier:
    default_args = {
        'model_def_file': '{}/model'.format(DATA_DIRNAME),
        'class_labels_file': '{}/labels.txt'.format(DATA_DIRNAME)
    }
    for k, v in default_args.items():
        if not os.path.exists(v):
            raise Exception("File {} not found at {}".format(k, v))

    def __init__(self, model_def_file, class_lables_file):
        logging.info('Loading model data and labels...')

        with tf.Graph().as_default(), tf.device('cpu:0'):
            self.sess = tf.Session()
            self.image_buffer = tf.placeholder(tf.string)
            image = tf.image.decode_jpeg(self.image_buffer, channels=3)
            image = tf.image.convert_image_dtype(image, dtype=tf.float32)
            image = self.eval_image(image, 299, 299)
            image = tf.sub(image, 0.5)
            image = tf.mul(image, 2.0)
            images = tf.expand_dims(image, 0)

            # Run inference with Inception v3 model

    def eval_image(self, image, height, width, scope=None):
        """Prepare one image for evaluation.
        Args:
          image: 3-D float Tensor
          height: integer
          width: integer
          scope: Optional scope for op_scope.
        Returns:
          3-D float Tensor of prepared image.
        """
        with tf.op_scope([image, height, width], scope, 'eval_image'):
            # Crop the central region of the image with an area containing 87.5% of
            # the original image.
            image = tf.image.central_crop(image, central_fraction=0.875)

            # Resize the image to the original height and width.
            image = tf.expand_dims(image, 0)
            image = tf.image.resize_bilinear(image, [height, width],
                                             align_corners=False)
            image = tf.squeeze(image, [0])
            return image


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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            res = make_response(jsonify(message='Image upload successfully!'), 201)
            return res

            # Convolutional
            # input = '--- Image data here ---'
            # output = convolutional(input)
            # return jsonify(result=output)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
