import os
import random
import string

import gridfs

from eve import Eve
from flask import jsonify, request, redirect, flash
from flask.helpers import make_response
from werkzeug.utils import secure_filename

from classifier import clf
from settings import (UPLOAD_FOLDER, ALLOWED_EXTENSIONS,
                      CODE_CLASSIFY_SUCCESS, MESSAGE_CLASSIFY_SUCCESS,
                      HOST, PORT)

app = Eve()
app.config['SECRET_KEY'] = "7;RE:]@xL_lp^TybQjfsq&'5M,!h\x0c+/S"
# app.config['DEBUG'] = True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_token(users):
    """
    Add a token when POST (register) /users
    """
    pool = string.ascii_letters + string.digits
    for user in users:
        user["token"] = ''.join(random.sample(pool, 32))


def gen_classification_result(documents):
    """
    Perform classification and write result when POST (upload) /images
    """
    for document in documents:
        image_object = document.get('image')
        fs = gridfs.GridFS(app.data.driver.db)
        image_data = fs.get(image_object)
        result = clf.classify_image(image_data.read())
        document['result'] = result


def post_image_upload_callback(request, payload):
    """
    Add extra information when successfully classify the image
    """
    print('test')


# Subscribe event hooks
app.on_insert_users += add_token
app.on_insert_images += gen_classification_result
app.on_post_post_images += post_image_upload_callback


@app.route('/images-demo', methods=['GET', 'POST'])
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
            file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            file.save(file_path)

            # Start classify image
            ret = clf.classify_image(file_path, from_file=True)
            return make_response(jsonify(
                code=CODE_CLASSIFY_SUCCESS,
                message=MESSAGE_CLASSIFY_SUCCESS,
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


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
