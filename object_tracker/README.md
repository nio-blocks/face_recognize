TrackObjects
============
Grab a frame of video from a specified camera or video, find an object based on filtering defined in the block, and then output the centroid location of that object in the frame.

Properties
----------
- **camera**: Where to find the local camera to read from. Index 0 references the localhost default camera
- **ipcam**: Whether or not to use an IP Camera.
- **ipcam_address**: Address for where to find the IP camera.
- **video_ref**: File location of video to be processed
- **filters**: List of filters used for image processing and tracking
- **obj**: Name of object to be tracked, characterized by filter type and bands
- **filter_type**: HSV or RGB filter for defining the mask
- **filter_lo**: Low band of filter
- **filter_hi**: High band of filter


Inputs
------

Outputs
-------
- **track**: A signal containing the object and it's reference coordinates in the frame.

Commands
--------

Dependencies
------------
-    opencv-python
-    imutils
-    numpy
-    enum

Input Example
-------------

Output Example
--------------
```
{
  'track': {
            'object': 'Object1',
            'y_coord': 37,
            'x_coord': 86
  }
}
```

range-detector.py
=================
Python script from the imutils library to help determine upper/lower bounds for
the TrackObjects filter properties.

Running this script will load 3 windows:
- **Original**: A copy of the image designated by -i flag
- **Thresh**: A copy of the image designated by the -i flag with maximum mask thresholds.
- **Trackbars**:  Draggable track bars to modify the mask threshold values.

The goal in adjusting the filters via the track bar should be to isolate the object(s)
you intend to track using the TrackObjects block.  

Once you are satisfied with your filters, press 'q' on the keyboard, and the two filter bands,
(low and high), will be printed in the window where you entered the command to run the script.

Example Output:
```
[0, 0, 0]
[255, 255, 255]
```

Flags
-----
- **-f Filter Type**: Flag for filter type, with two options.  HSV or RGB
- **-i Image**: Flag for reference to the image

Example Command
---------------
```
python3 range-detector.py -f HSV -i ~/Documents/TestImage/image.jpg
```
