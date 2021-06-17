import os
from datetime import datetime

from flask import current_app
from flask_login import current_user
from werkzeug.utils import secure_filename

from ml.ml_services.main import str_face_detection, \
    str_face_recognition, str_emotion_recognition, str_human_detection


def find_name():
    return current_user.username + datetime.now().strftime('%y%m%d%h%M%s') + '.webm'


def find_path(filename):
    return os.path.join(current_app.root_path, 'static', 'files', filename)


def find_source_video_address(file):
    filename = secure_filename(file.filename)
    file_address = os.path.join(current_app.root_path, filename)
    return file_address


def save_video(file, file_address):
    file.save(file_address)


def default_requested_services():
    return {str_face_detection: True,
            str_face_recognition: True,
            str_emotion_recognition: True,
            str_human_detection: True
            }


def find_requested_services(form):
    return {str_face_detection: True,
            str_face_recognition: True,
            str_emotion_recognition: True,
            str_human_detection: True
            }
