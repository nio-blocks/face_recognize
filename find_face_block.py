import face_recognition
import pickle
import base64
import numpy

from nio.block.base import Block
from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.block.terminals import input
from nio.properties import VersionProperty, BoolProperty, Property, \
                            FloatProperty


@input('known')
@input('unknown')
class FindFace(EnrichSignals, Block):

    version = VersionProperty("2.1.0")
    accuracy = FloatProperty(title='Comparison Accuracy', default=0.6)
    location = BoolProperty(title='Output Face Location', default=False)
    capture = Property(title='Image', default='{ $frame }')

    def __init__(self):
        super().__init__()
        self.ref_names = []
        self.ref_encodings = []

    def process_signals(self, signals, input_id):
        if input_id == 'known':
            for signal in signals:
                self.ref_names = []
                self.ref_encodings = []
                for face in signal.faces:
                    name = face['name']
                    for encoding in face['encoding']:
                        self.ref_names.append(name)
                        self.ref_encodings.append(
                            pickle.loads(base64.b64decode(encoding)))

        if input_id == 'unknown':
            new_signals = []
            for signal in signals:
                frame = numpy.array(self.capture(signal))
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(
                    frame, face_locations)

                # Set a default signal if no faces are found
                if self.location():
                    out = self.get_output_signal(
                        {'found': ['None'], 'location': [[0, 0, 0, 0]]}, signal)
                else:
                    out = self.get_output_signal({'found': ['None']}, signal)

                names = []
                locations = []
                if len(face_encodings) > 0:
                    for e in range(len(face_encodings)):
                        # Compare unknown face with all known face encodings
                        match = face_recognition.compare_faces(
                            self.ref_encodings,
                            face_encodings[e],
                            self.accuracy()
                        )
                        name = 'Unknown'

                    # Grab the name of the matched face
                    for i in range(len(match)):
                        if match[i]:
                            name = self.ref_names[i]

                        names.append(name)
                        # Get the location and format it nicely
                        location = [
                            face_locations[e][0],
                            face_locations[e][1],
                            face_locations[e][2],
                            face_locations[e][3]
                        ]
                        locations.append(location)

                    # Add list of found names (and locations) to output signal
                    if self.location():
                        out = self.get_output_signal(
                            {'found': names, 'location': locations}, signal)
                    else:
                        out = self.get_output_signal({'found': names}, signal)
                new_signals.append(out)
            self.notify_signals(new_signals)
