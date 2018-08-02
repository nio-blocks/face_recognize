import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestFindFace(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        sys.modules['face_recognition'] = MagicMock()
        from ..find_face_block import FindFace
        global FindFace

    def test_face_find_known_input(self):
        # The 'known' input does not spit out a signal
        blk = FindFace()
        with patch(FindFace.__module__ + '.base64') as mock_base64, \
                patch(FindFace.__module__ + '.pickle') as mock_pickle:
            mock_base64.b64decode.return_value = b'\signal'
            mock_pickle.loads.return_value = 'pickleReturn'

            self.configure_block(blk, {})
            blk.start()
            blk.process_signals(
                [Signal({
                    'faces': [{
                        'name': 'Billy',
                        'id': '123id4me',
                        'encoding': ['456encodingSticks'],
                        'user_id': 'bobby_1'
                    }]
                })],
                input_id='known'
            )
            self.assert_num_signals_notified(0)
            mock_base64.b64decode.assert_called_with('456encodingSticks')
            mock_pickle.loads.assert_called_with(b'\signal')
            blk.stop()

    def test_face_find_unknown_input(self):
        blk = FindFace()
        blk.ref_names = ['Billy', 'Bob']
        with patch(FindFace.__module__ + '.base64') as mock_base64, \
                patch(FindFace.__module__ + '.face_recognition') as mock_face:
            mock_base64.b64encode.return_value.decode.return_value = 'signal'
            mock_face.face_encodings.return_value = ['encode1', 'encode2']
            mock_face.compare_faces.return_value = ['Billy', 'Bob']

            self.configure_block(blk, {})
            blk.start()
            blk.process_signals(
                [Signal({'frame': MagicMock()})], input_id='unknown')
            self.assert_num_signals_notified(1)
            self.assert_last_signal_list_notified(
                [Signal({'found': ['Billy', 'Bob']})])
            blk.stop()
