import cv2

import face_recognition

from ml.ml_services.emotion_recognition import EmotionRecognition
from ml.ml_services.face_detection import FaceDetection
from ml.ml_services.facerecognition import FaceRecognition
from ml.ml_services.human_detection import HumanDetection


# declare services types
str_face_detection = 'face_detection'
str_face_recognition = 'face_recognition'
str_emotion_recognition = 'emotion_recognition'
str_human_detection = 'human_detection'
str_camera = 'camera'
str_video = 'video'

import os
dirname = os.path.dirname(__file__)
print(dirname)
filename2 = os.path.join(dirname, 'raziyeh.jpg')
print(filename2)
# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file(filename2)
# Load a sample picture and learn how to recognize it.

obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Create arrays of known face encodings and their names
global_known_face_encodings = [
    obama_face_encoding]

global_known_face_names = [
    "raziyeh"
]


class MLServices:
    def __init__(self, source_address, result_address):
        # load models
        self.face_detection_model = FaceDetection()
        self.face_recognition_model = FaceRecognition(global_known_face_encodings, global_known_face_names)
        self.emotion_recognition_model = EmotionRecognition()
        self.human_detection_model = HumanDetection()
        self.source_address = source_address
        self.result_address = result_address
        # create a VideoCapture object for reading video file or camera frames
        self.source = cv2.VideoCapture(source_address)

        # We need to set resolutions. so, convert them from float to integer.
        frame_width = int(self.source.get(3))
        frame_height = int(self.source.get(4))
        size = (frame_width, frame_height)

        # Below VideoWriter object will create a frame of above defined
        # The output is stored in result_address file file.
        self.result = cv2.VideoWriter(result_address, cv2.VideoWriter_fourcc(*'vp90'), 10, size)

    def __del__(self):
        # Release the camera or video reader
        self.source.release()

        # Release the result writer
        self.result.release()

    def start_services_camera(self, services):
        while True:
            # read the video or camera frame
            ret, frame = self.source.read()
            if not ret:
                break
            else:
                if str_face_detection in services:
                    ret, frame = self.face_detection_model.detect_faces(ret, frame)

                if str_face_recognition in services:
                    ret, frame = self.face_recognition_model.recognize_faces(ret, frame)

                if str_emotion_recognition in services:
                    ret, frame = self.emotion_recognition_model.recognize_emotion(ret, frame)

                if str_human_detection in services:
                    ret, frame = self.human_detection_model.detect_humans(ret, frame)

                self.result.write(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                # concat frame one by one and show result
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def start_services(self, services, input_type):
        while True:
            # read the video or camera frame
            ret, frame = self.source.read()
            if not ret:
                break
            else:
                if str_face_detection in services:
                    ret, frame = self.face_detection_model.detect_faces(ret, frame)

                if str_face_recognition in services:
                    ret, frame = self.face_recognition_model.recognize_faces(ret, frame)

                if str_emotion_recognition in services:
                    ret, frame = self.emotion_recognition_model.recognize_emotion(ret, frame)

                if str_human_detection in services:
                    ret, frame = self.human_detection_model.detect_humans(ret, frame)
                self.result.write(frame)
