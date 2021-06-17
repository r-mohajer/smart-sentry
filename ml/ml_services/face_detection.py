import os

import cv2


class FaceDetection(object):
    model = cv2.CascadeClassifier(
        os.path.join(os.path.dirname(os.path.dirname(__file__)),
                     'models/haarcascade_frontalface_default.xml'))

    def detect_faces(self, ret, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = self.model.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return ret, frame