import face_recognition
from nio import Block
from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.properties import VersionProperty, BoolProperty, Property, \
                            FloatProperty


class FindFace(EnrichSignals, Block):

    version = VersionProperty('0.1.0')

    def process_signal(self, signal):
        face_locations = face_recognition.face_locations(signal.frame)
        signal.faces = face_locations
        return signal
