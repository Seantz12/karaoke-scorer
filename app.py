import numpy as np
import os
import sys

from aubio import (
    source, pitch
)
from flask import (
    Flask, request, jsonify
)
app = Flask(__name__)

@app.route("/")
def main():
    return "Don't visit here!"

def process_pitches(file_name):
    downsample = 1
    samplerate = 44100 // downsample

    win_s = 4096 // downsample
    hop_s = 512 // downsample

    s = source(file_name, samplerate, hop_s)

    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        curr_pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        # print("%f %f %f" % (total_frames / float(samplerate), curr_pitch, confidence))
        pitches += [curr_pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    return pitches


@app.route("/compare", methods = ['POST'])
def recieve_request():
    # save files
    random_number = str(np.random.rand())
    source_file_name = './audio_source{}.wav'.format(random_number)
    compare_file_name = './audio_compare{}.wav'.format(random_number)
    audio_data_source = request.files['source']
    audio_data_source.save(source_file_name)
    audio_data_compare = request.files['compare']
    audio_data_compare.save(compare_file_name)

    source_pitches = process_pitches(source_file_name)
    compare_pitches = process_pitches(compare_file_name)

    print(source_pitches)
    print(compare_pitches)


    if os.path.exists(source_file_name):
        os.remove(source_file_name)
    if os.path.exists(compare_file_name):
        os.remove(compare_file_name)
    response = jsonify(score=100)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
