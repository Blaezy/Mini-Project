from flask_cors import CORS
from flask import Flask, jsonify, send_file, request, render_template
from werkzeug.serving import WSGIRequestHandler
import os
import time

from matplotlib.image import imsave

from srgan import generator

from common import resolve_single
from utils import load_image


weights_dir = 'weights/srgan'
def weights_file(filename): return os.path.join(weights_dir, filename)


gan_generator = generator()
gan_generator.load_weights(weights_file('gan_generator.h5'))


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():

    return render_template('index.html')

    return jsonify({'message': 'Hello world!'})


@app.route('/generate', methods=["GET", "POST"])
def generate():

    global gan_generator

    imgData = request.get_data()

    with open("input.png", 'wb') as output:
        output.write(imgData)

    lr = load_image("input.png")
    gan_sr = resolve_single(gan_generator, lr)
    epoch_time = int(time.time())
    outputfile = 'output_%s.png' % (epoch_time)
    imsave(outputfile, gan_sr.numpy())
    response = {'result': outputfile}
    return jsonify(response)


@app.route('/download/<fname>', methods=['GET'])
def download(fname):
    return send_file(fname, as_attachment=True)


if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
