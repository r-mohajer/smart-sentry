from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from smart_sentry import db, login_manager


class User(db.Document, UserMixin):
    # User authentication information
    email = db.StringField(max_length=30)
    username = db.StringField(default='')
    password = db.StringField()

    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')
    # profile_image = db.

    # Relationships
    roles = db.ListField(db.StringField(), default=[])

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"  # '{self.image_file}'


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class Video(db.Document, UserMixin):
    file = db.FileField()
