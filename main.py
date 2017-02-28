from flask import Flask, jsonify

app = Flask(__name__)


def convolutional(input):
    return input


@app.route('/api/image', methods=['POST'])
def plantpano():
    input = '--- Image data here ---'
    output = convolutional(input)
    return jsonify(result=output)


@app.route('/', methods=['GET'])
def main():
    return 'Hello PlantPano!'


if __name__ == '__main__':
    app.run()
