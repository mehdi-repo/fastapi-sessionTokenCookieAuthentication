
from sqlalchemy.orm import Session
from model.userModel import User
from typing import  Dict,Any
from security.authSecurity import verify_password


def create_user(db: Session,signup:User) -> bool:
        try:
            db.add(signup)
            db.commit()
        except:
            return False
        return True

def get_user_by_username(db: Session,username:str):
    return db.query(User).filter(User.username==username).first()




def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
