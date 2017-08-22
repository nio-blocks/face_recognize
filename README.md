CaptureFrame
============
Grab a frame of video from a specified camera and send the frame data as a signal.

Properties
----------
- **camera**: Where to find the local camera to read from.
- **ipcam**: Whether or not to use an IP Camera.
- **ipcam_address**: Address for where to find the IP camera.

Inputs
------
- **default**: Any signal to trigger a frame being grabbed from the specified camera.

Outputs
-------
- **default**: A signal containing the serialized and stringified video frame.

Commands
--------

Dependencies
------------
- numpy
- opencv-python

FindFace
========
Grab a frame of video from a specified camera, find a face encoding within the frame, compare the encoding with encoding of known faces from an input signal, output a signal containing the name of the found face.

Properties
----------
- **accuracy**: Degree of confidence to shoot for when finding faces.
- **camera**: Where to find the local camera to read from.
- **frame_size**: Scaling factor for frame.
- **image**: Whether or not to use an IP Camera.
- **ipcam**: Whether or not to use an IP Camera.
- **ipcam_address**: Address for where to find the IP camera.
- **location**: Include coordinate location of face on output signal.

Inputs
------
- **known**: Signal to add the known face encodings and names to compare found faces against. Expects a 'faces' object which contains a list of objects with attributes 'name', 'user_id', 'id', and 'encoding'.
- **unknown**: Signal to begin collecting frames from the camera and search for faces.

Outputs
-------
- **default**: A signal containing the name of the face identified from the webcam.

Commands
--------

Dependencies
------------
- face_recognition
- numpy
- opencv-python

Input Example
-------------
```
{
 'faces': [
  {
   'name': 'Barack',
   'user_id': 'bobama',
   'id': '4999011a-8ded-49c4-a927-77a09dcdb578',
   'encoding': 'gANjbnVtcHkuY29yZS5tdWx0aWFycmF5Cl9yZWNvbn...'
  }
 ]
}
```

Output Example
--------------
```
{
 'found': 'Barack'
}
```


GetEncodingFromFile
===================
A block for running mongo commands

Properties
----------
- **image_paths**: Full path to the image file that will be added.
- **sname**: Name of the face being added to the database.
- **uid**: Id of the face being added to the database.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A signal containing the facial encoding, user id, and name.

Commands
--------

Dependencies
------------
- face_recognition

Output Example
--------------
```
{
 'encoding': 'gANjbnVtcHkuY29yZS5tdWx0aWFycmF5Cl9yZWNvbn...',
 'name': 'Barack',
 'user_id': 'bobama'
}
```
