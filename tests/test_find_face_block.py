from unittest.mock import patch, Mock
from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..find_face_block import FindFace


class TestFindFace(NIOBlockTestCase):

    @patch(FindFace.__module__ + '.face_recognition')
    def test_face_locations(self, mock_face):
        """ For every input frame, faces are located and added to
        .the signal
        """
        dummy_frame = Mock()
        dummy_locations = [('T', 'R', 'B', 'L')]
        mock_face.face_locations.return_value = dummy_locations

        blk = FindFace()
        self.configure_block(blk, {
            'upsample': 7,
        })
        blk.start()
        blk.process_signals([
            Signal({'frame': dummy_frame}),
        ])
        blk.stop()
        mock_face.face_locations.assert_called_once_with(dummy_frame, 7)
        self.assert_num_signals_notified(1)
        self.assert_last_signal_list_notified([
            Signal({'frame': dummy_frame, 'faces': [('L', 'T', 'R', 'B')]}),
        ])
