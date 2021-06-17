from flask import render_template, Blueprint, current_app, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ml.ml_services.main import MLServices, str_face_detection, str_video, str_camera, \
    str_face_recognition, str_emotion_recognition, str_human_detection
from smart_sentry.ml_api.forms import VideoForm, ChooseServicesForm
from smart_sentry.ml_api.utils import find_name, find_path, save_video, \
    find_requested_services, default_requested_services

ml_api = Blueprint('ml_api', __name__)


@ml_api.route('/video_feed')
def video_feed():
    ml_service = MLServices(0, find_path(find_name()))
    return Response(ml_service.start_services_camera([str_face_detection]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@ml_api.route("/face/detection/camera")
@login_required
def face_detection_camera():
    return render_template('single_feature_camera.html', title='Face Detection - Camera')


@ml_api.route("/face/detection/file", methods=['GET', 'POST'])
@login_required
def face_detection_file():
    form = VideoForm()
    if form.validate_on_submit():
        f = form.video.data
        source_path = find_path(secure_filename(f.filename))
        save_video(f, source_path)
        result_name = find_name()
        result_path = find_path(result_name)
        ml_service = MLServices(source_path, result_path)
        ml_service.start_services([str_face_detection], str_video)
        return render_template('video_player.html', title='Face Detection - File', form=form, filename=result_name)
    return render_template('single_feature_video.html', title='Face Detection - File', form=form)


@ml_api.route('/video_feed/human_detection')
def video_feed_human_detection():
    ml_service = MLServices(0, find_path(find_name()))
    return Response(ml_service.start_services_camera([str_human_detection]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@ml_api.route("/human/detection/camera")
@login_required
def human_detection_camera():
    return render_template('single_feature_camera.html', title='Face Detection - Camera')


@ml_api.route("/human/detection/file", methods=['GET', 'POST'])
@login_required
def human_detection_file():
    form = VideoForm()
    if form.validate_on_submit():
        f = form.video.data
        source_path = find_path(secure_filename(f.filename))
        save_video(f, source_path)
        result_name = find_name()
        result_path = find_path(result_name)
        ml_service = MLServices(source_path, result_path)
        ml_service.start_services([str_human_detection], str_video)
        return render_template('video_player.html', title='Human Detection - File', form=form, filename=result_name)
    return render_template('single_feature_video.html', title='Human Detection - File', form=form)


@ml_api.route('/video_feed/face_recognition')
def video_feed_face_recognition():
    ml_service = MLServices(0, find_path(find_name()))
    return Response(ml_service.start_services_camera([str_face_recognition]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@ml_api.route("/face/recognition/camera")
@login_required
def face_recognition_camera():
    return render_template('face_recognition_camera.html', title='Face Detection - Camera')


@ml_api.route("/face/recognition/file", methods=['GET', 'POST'])
@login_required
def face_recognition_file():
    form = VideoForm()
    if form.validate_on_submit():
        f = form.video.data
        source_path = find_path(secure_filename(f.filename))
        save_video(f, source_path)
        result_name = find_name()
        result_path = find_path(result_name)
        ml_service = MLServices(source_path, result_path)
        ml_service.start_services([str_face_recognition], str_video)
        return render_template('video_player.html', title='Face Recognition - File', form=form, filename=result_name)
    return render_template('face_recognition_video.html', title='Face Recognition - File', form=form)


@ml_api.route('/video_feed/emotion_recognition')
def video_feed_emotion_recognition():
    ml_service = MLServices(0, find_path(find_name()))
    return Response(ml_service.start_services_camera([str_emotion_recognition]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@ml_api.route("/emotion/recognition/camera")
@login_required
def emotion_recognition_camera():
    return render_template('emotion_recognition_camera.html', title='Emotion Detection - Camera')


@ml_api.route("/emotion/recognition/file", methods=['GET', 'POST'])
@login_required
def emotion_recognition_file():
    form = VideoForm()
    if form.validate_on_submit():
        f = form.video.data
        source_path = find_path(secure_filename(f.filename))
        save_video(f, source_path)
        result_name = find_name()
        result_path = find_path(result_name)
        ml_service = MLServices(source_path, result_path)
        ml_service.start_services([str_emotion_recognition], str_video)
        return render_template('video_player.html', title='Emotion Recognition - File', form=form, filename=result_name)
    return render_template('emotion_recognition_video.html', title='Emotion Recognition - File', form=form)


@ml_api.route('/video_feed_all')
def video_feed_all():
    ml_service = MLServices(0, find_path(find_name()))
    return Response(ml_service.start_services_camera(
        [str_face_recognition, str_emotion_recognition, str_human_detection]),
        mimetype='multipart/x-mixed-replace; boundary=frame')


@ml_api.route("/Processor/camera")
@login_required
def all_services_camera():
    form = ChooseServicesForm()
    requested_services = default_requested_services()
    if form.validate_on_submit():
        requested_services = find_requested_services(form)
    return render_template('all_features_camera.html', title='Camera Video Processor',
                           services=requested_services)


@ml_api.route("/Processor/file", methods=['GET', 'POST'])
@login_required
def all_services_video():
    form = VideoForm()
    if form.validate_on_submit():
        f = form.video.data
        source_path = find_path(secure_filename(f.filename))
        save_video(f, source_path)
        result_name = find_name()
        result_path = find_path(result_name)
        ml_service = MLServices(source_path, result_path)
        ml_service.start_services([str_face_recognition,
                                   str_emotion_recognition, str_human_detection],
                                  str_video)
        return render_template('video_player.html', title='Video Processor - File', form=form, filename=result_name)
    return render_template('single_feature_video.html', title='Video Processor - File', form=form)
