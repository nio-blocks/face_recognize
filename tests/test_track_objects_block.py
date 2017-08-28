from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from unittest.mock import patch, MagicMock
import sys


class TestTrackObjects(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        sys.modules['imutils'] = MagicMock()
        from ..object_tracker.track_objects_block import TrackObjects
        global TrackObjects

    def test_track_one_object(self):
        blk = TrackObjects()
        with patch(TrackObjects.__module__ + '.cv2') as patch_cv2, \
                patch(TrackObjects.__module__ + '.imutils.resize') as patch_im:

            patch_cv2.VideoCapture.return_value.read.return_value = ('g', 'f')
            patch_cv2.minEnclosingCircle.return_value = ((156, 225), 10.2)
            patch_im.resize.return_value = 'frame.jpg'

            self.configure_block(blk, {
                'ipcam': True,
                'ipcam_address': 'ipcamAddress',
                'filters': [{
                    'obj': 'testObject',
                    'filter_type': 'HSV',
                    'filter_hi': [255, 255, 255],
                    'filter_lo': [1, 1, 1]
                }]
            })
            blk.start()
            blk.process_signals([Signal({
                'sim': 1
            })])
            self.assert_num_signals_notified(1)
            blk.stop()

    def test_track_multiple_objects(self):
        blk = TrackObjects()
        with patch(TrackObjects.__module__ + '.cv2') as patch_cv2, \
                patch(TrackObjects.__module__ + '.imutils.resize') as patch_im:

            patch_cv2.VideoCapture.return_value.read.return_value = ('g', 'f')
            patch_cv2.minEnclosingCircle.return_value = ((156, 225), 10.2)
            patch_im.resize.return_value = 'frame.jpg'

            self.configure_block(blk, {
                'ipcam': True,
                'ipcam_address': 'ipcamAddress',
                'filters': [{
                    'obj': 'Object1',
                    'filter_type': 'HSV',
                    'filter_hi': [255, 255, 255],
                    'filter_lo': [1, 1, 1]
                    },
                    {
                    'obj': 'Object2',
                    'filter_type': 'HSV',
                    'filter_hi': [100, 100, 100],
                    'filter_lo': [10, 10, 10]
                    }]
            })
            blk.start()
            blk.process_signals([Signal({
                'sim': 1
            })])
            self.assert_num_signals_notified(2)
            blk.stop()

    def test_track_none(self):
        blk = TrackObjects()
        with patch(TrackObjects.__module__ + '.cv2') as patch_cv2, \
                patch(TrackObjects.__module__ + '.imutils.resize') as patch_im:

            patch_cv2.VideoCapture.return_value.read.return_value = ('g', 'f')
            patch_cv2.minEnclosingCircle.return_value = ((156, 225), 10.2)
            patch_im.resize.return_value = 'frame.jpg'

            self.configure_block(blk, {
                'ipcam': False,
                'filters': [{
                    'obj': 'testObject',
                    'filter_type': 'HSV',
                    'filter_hi': [255, 255, 255],
                    'filter_lo': [1, 1, 1]
                }]
            })
            blk.start()
            blk.process_signals([Signal({
                'sim': 1
            })])
            self.assert_num_signals_notified(1)
            self.assert_last_signal_notified(Signal({
                'track': {
                    'object': 'testObject',
                    'x_coord': None,
                    'y_coord': None
                }
            }))
            blk.stop()
