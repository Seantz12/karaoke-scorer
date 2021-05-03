# coding=utf-8

import sys
import logging

from aubio import source, pitch


class PitchController:

    DOWNSAMPLE = 1
    SAMPLE_RATE = 44100 // DOWNSAMPLE

    WIN_S = 4096 // DOWNSAMPLE
    HOP_S = 512 // DOWNSAMPLE

    TOLERANCE = 0.8

    def process(self):

        s = source("audio_source.wav", self.SAMPLE_RATE, self.HOP_S)

        pitch_o = pitch(
            "yin", self.WIN_S, self.HOP_S, s.samplerate
        )
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(self.TOLERANCE)

        pitches = []
        confidences = []
        total_frames = 0

        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()
            logging.info(
                "%f %f %f",
                total_frames / float(s.samplerate),
                pitch,
                confidence
            )
            pitches += [pitch]
            confidences += [confidence]
            total_frames += read
            if read < hop_s:
                break

        return pitches

