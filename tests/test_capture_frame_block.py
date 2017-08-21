import sys
from unittest.mock import patch, MagicMock

from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestCaptureFrame(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        from ..capture_frame_block import CaptureFrame
        global CaptureFrame

    def test_capture_frame(self):

        blk = CaptureFrame()
        with patch(CaptureFrame.__module__ + '.cv2.VideoCapture') as mock_video_capture, \
                patch(CaptureFrame.__module__ + '.base64') as mock_base64:
            mock_video_capture.return_value.read.return_value = 'bytes', 'frameBytes'
            mock_base64.b64encode.return_value.decode.return_value = 'signal'

            self.configure_block(blk, {})
            blk.start()
            blk.process_signals([Signal()])

            self.assert_num_signals_notified(1)
            self.assert_last_signal_notified(Signal({
                'capture': 'signal'
            }))
            blk.stop()

        # Does this also need to test when self.ipcam() = True?
