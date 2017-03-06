from flask import Flask, jsonify, request, make_response, redirect, flash
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# Flask confs
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
