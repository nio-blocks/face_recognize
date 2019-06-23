import face_recognition
from nio import Block
from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.properties import VersionProperty, BoolProperty, Property, \
                            FloatProperty


class FindFace(EnrichSignals, Block):

    version = VersionProperty('0.1.0')

    def process_signal(self, signal):
        face_locations = face_recognition.face_locations(signal.frame)
        # bounding boxes are (top, right, bottom, left)
        # pil blocks use (left, upper, right, lower)
        locations = []
        for location in face_locations:
            locations.append(
                (location[3], location[0], location[1], location[2]))
        signal.faces = locations
        return signal
