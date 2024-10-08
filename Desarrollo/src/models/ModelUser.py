from .entities.User import User
class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, password, fullname, telefono, perfil FROM user WHERE email = '{}'".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                user=User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4], row[5])
                return user
            else:
                return None
        except Exception as e:
            raise Exception(e)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, fullname, telefono, perfil FROM user WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2], row[3], row[4])
            else:
                return None
        except Exception as e:
            raise Exception(e)

    @classmethod
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO user (password, fullname, telefono, email, perfil) VALUES (%s, %s, %s, %s, %s)"
            values = (user.password, user.fullname, user.telefono, user.email, user.perfil)
            cursor.execute(sql, values)
            db.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False