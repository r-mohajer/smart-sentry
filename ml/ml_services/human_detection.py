from __future__ import print_function
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
face_cascade = cv2.CascadeClassifier('/home/raziyeh/Machine-Learning/opencv-test-project/haarcascade_frontalface_default.xml')


class HumanDetection(object):
    def detect_humans(self, ret, image):
        orig = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        return ret, image


# In[4]:
# get and video and detect and recognize faces
def detect_humans_video(video_source):
    # Load face recognition model
    model = HumanDetection()
    video_capture = cv2.VideoCapture(video_source)
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    size = (frame_width, frame_height)
    result = cv2.VideoWriter('human_detection.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
    while video_capture.isOpened():
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frame = model.detect_humans(ret, frame)

        result.write(frame)
        print(frame)
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_humans_video(0)