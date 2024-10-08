from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id=None, email="", password="", fullname="", telefono="", perfil="") -> None:
        self.id = id
        self.email = email
        self.password = password
        self.fullname = fullname
        self.telefono = telefono
        self.perfil = perfil


    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)