#-*-conding:utf-8-*-

import cv2
import numpy as np
import os
import configparser


root_dir=os.path.abspath(os.path.dirname(__file__))
configpath = os.path.join(root_dir, "config.txt")
config = configparser.ConfigParser()
config.read(configpath)
# The actual distance from the object of the prior image to the camera
KNOWN_DISTANCE = float(config.get("Prior_image","KNOWN_DISTANCE"))
# The actual width of the object in the prior image
KNOWN_WIDTH = float(config.get("Prior_image","KNOWN_WIDTH"))
image_path = config.get("Prior_image","image_path")
Classifier_path = config.get("face_classifier", "Classifier_path")
face_cascade = cv2.CascadeClassifier(Classifier_path)

class MonocularRanging:

    def find_marker(self, img):
        global cnt
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        if len(faces) > 0:
            for faceRect in faces:
                x, y, w, h = faceRect
                cnt = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return cv2.minAreaRect(cnt)

    def distance_to_camera(self, knownWidth, focalLength, perWidth):
        # compute and return the distance from the object to the camera
        return (knownWidth * focalLength) / perWidth

    def focal_length(self, image, known_distance, known_width):
        marker = self.find_marker(image)
        cv2.imshow("img", image)
        #The pixel width of the object in the image is marker[1][0]
        focalLength = (marker[1][0] * known_distance) / known_width
        print('focalLength = ', focalLength)
        return focalLength

    def show(self, marker, frame, distance):
        box = cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        cv2.putText(frame, "%.2fcm" % (distance),
                    (frame.shape[1] - 150, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0, 255, 0), 2)
        # show a frame
        cv2.imshow("capture", frame)

# The picture taken by this camera is used for a priori
image = cv2.imread(image_path)
M = MonocularRanging()
focallength = M.focal_length(image, KNOWN_DISTANCE, KNOWN_WIDTH)
camera = cv2.VideoCapture(0)
while camera.isOpened():
    # get a frame
    (grabbed, frame) = camera.read()
    marker = M.find_marker(frame)
    if marker == 0:
        continue
    distance = M.distance_to_camera(KNOWN_WIDTH, focallength, marker[1][0])
    M.show(marker, frame, distance)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
