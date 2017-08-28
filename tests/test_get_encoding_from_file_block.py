import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestCaptureFrame(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['face_recognition'] = MagicMock()
        from ..face_recognize.get_encoding_from_file_block import \
            GetEncodingFromFile
        global GetEncodingFromFile

    def test_get_encoding_from_file(self):
        blk = GetEncodingFromFile()
        with patch(GetEncodingFromFile.__module__ + '.base64') as mock_base64,\
                patch(GetEncodingFromFile.__module__ + '.face_recognition') as\
                mock_face:
            mock_base64.b64encode.return_value.decode.return_value = \
                'serializedEncoding'
            mock_face.face_encodings.return_value = ['image_file']

            self.configure_block(blk, {
                'image_paths': '{{ $image_paths }}',
                'sname': '{{ $sname }}',
                'uid': '{{ $uid }}',
            })

            blk.start()
            blk.process_signals([Signal({
                'image_paths': ['path1'],
                'sname': 'saveName',
                'uid': 'userID',
            })])
            self.assert_num_signals_notified(1)
            self.assert_last_signal_notified(Signal({
                'user_id': 'userID',
                'name': 'saveName',
                'encoding': ['serializedEncoding']
            }))
            blk.stop()
