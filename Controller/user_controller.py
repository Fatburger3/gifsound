from Model.models import *
from Controller.session_controller import *


def create_user_table():
    Base.metadata.create_all(bind=get_engine())


def get_user(user_id):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id)
    except exc.SQLAlchemyError:
        return False
    return user


def get_all_users():
    session = get_session()
    try:
        users = session.query(User).all()
    except exc.SQLAlchemyError:
        return False
    return users


def create_user(username, email, password, role):
    user = User()
    user.username = username
    user.email = email
    user.password = password
    user.role = role
    try:
        session_commit(user)
    except exc.SQLAlchemyError:
        return False


