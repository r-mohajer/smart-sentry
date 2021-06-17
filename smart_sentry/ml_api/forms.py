from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, BooleanField
from wtforms.fields.html5 import URLField
from wtforms.validators import URL, DataRequired


class VideoForm(FlaskForm):
    video = FileField('Choose video file', validators=[FileAllowed(['mp4']), FileRequired()])
    submit = SubmitField('Upload')


class UploadImageForm(FlaskForm):
    video = FileField('Upload image file', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')


class GetLinkForm(FlaskForm):
    url = URLField('Image or video url', validators=[URL()])
    submit = SubmitField('Upload')


class ChooseServicesForm(FlaskForm):
    face_detection = BooleanField('Face Detection')
    face_recognition = BooleanField('Face Recognition')
    emotion_recognition = BooleanField('Emotion Recognition')
    human_detection = BooleanField('Human Detection')
    submit = SubmitField('Process')
