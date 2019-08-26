# Monocular-Visual-Odometry
The distance from the object to the monocular camera is roughly estimated by opencv.
## Environment
* OpenCV
* Numpy
## Usage
* A priori image is acquired through this camera.

* config.txt<br>
  KNOWN_DISTANCE : The actual distance from the object of the prior image to the camera<br>
  KNOWN_WIDTH : The actual width of the object in the prior image<br>
  image_path : Path to a priori image<br>
  Classifier_path : Path to a detector<br>
  
* python odometry.py<br>
  This example is based on opencv for face detection.The distance from the camera of the laptop to the face is measured.
