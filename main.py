import os

from eve import Eve
from flask import jsonify, request, redirect, flash
from flask.helpers import make_response
from werkzeug.utils import secure_filename

from classifier import clf
from hooks import add_token, gen_classification_result
from settings import (UPLOAD_FOLDER, ALLOWED_EXTENSIONS,
                      CODE_CLASSIFY_SUCCESS, MESSAGE_CLASSIFY_SUCCESS,
                      HOST, PORT)

app = Eve()
app.on_insert_users += add_token
app.on_insert_images += gen_classification_result
app.config['SECRET_KEY'] = "7;RE:]@xL_lp^TybQjfsq&'5M,!h\x0c+/S"
# app.config['DEBUG'] = True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
