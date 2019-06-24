import face_recognition
from nio import Block
from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.properties import VersionProperty, IntProperty


class FindFace(EnrichSignals, Block):

    upsample = IntProperty(
        title='Numer of Times to Upsample',
        default=1,
        advanced=True)
    version = VersionProperty('0.1.0')

    def process_signal(self, signal):
        frame = signal.frame
        upsample = self.upsample(signal)
        face_locations = face_recognition.face_locations(frame, upsample)
        # bounding boxes are (top, right, bottom, left)
        # pil blocks use (left, upper, right, lower)
        locations = []
        for location in face_locations:
            locations.append(
                (location[3], location[0], location[1], location[2]))
        signal.faces = locations
        return signal
