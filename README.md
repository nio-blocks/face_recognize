FindFace
========
Find a face encoding within a frame from an incoming signal, compare the encoding with encoding of known faces from an input signal, output a signal containing the name of the found face.

Properties
----------
- **accuracy**: Degree of confidence for finding faces.
- **enrich**: 
- **location**: Include coordinate location of face on output signal.

Inputs
------
- **known**: Signal to add the known face encodings and names to compare found faces against. Expects a 'faces' object which contains a list of objects with attributes 'name', 'user_id', 'id', and 'encoding'.
- **unknown**: Signal to with an image to search for faces.

Outputs
-------
- **default**: A signal containing the name of the identified face.

Commands
--------
None

Dependencies
------------
- face_recognition
- numpy

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

***

GetEncodingFromFile
===================
Load face image file and serialize the encoding.

Properties
----------
- **image_paths**: Full path to the image file that will be added.
- **sname**: Name of the face being added to the database.
- **uid**: Id of the face being added to the database.

Inputs
------
- **default**: Any list of signals with the path to the face image.

Outputs
-------
- **default**: A signal containing the facial encoding, user id, and name.

Commands
--------
None

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

