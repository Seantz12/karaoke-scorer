import uuid
import os
import logging

from controllers.compare import CompareController
from controllers.pitch import PitchController
from flask import (
    Flask, request, jsonify
)


app = Flask(__name__)

@app.route("/")
def main():
    return "Don't visit here!"


@app.route("/compare", methods = ['POST'])
def receive_request():
    # save files
    random_suffix = str(uuid.uuid4())
    source_file_name = './audio_source{}.wav'.format(random_suffix)
    compare_file_name = './audio_compare{}.wav'.format(random_suffix)
    audio_data_source = request.files['source']
    audio_data_source.save(source_file_name)
    audio_data_compare = request.files['compare']
    audio_data_compare.save(compare_file_name)

    pitch_controller = PitchController()

    source_pitches = pitch_controller.process(source_file_name)
    compare_pitches = pitch_controller.process(compare_file_name)

    logging.debug(source_pitches)

    compare_controller = CompareController()
    score_array = compare_controller.compare_pitches_direct(source_pitches, compare_pitches)
    print(score_array)

    if os.path.exists(source_file_name):
        os.remove(source_file_name)
    if os.path.exists(compare_file_name):
        os.remove(compare_file_name)
    response = jsonify(score=100)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
