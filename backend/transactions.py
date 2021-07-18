from models import (UserOrm, UserModel, UserWithHashModel)

def get_user_txn(session, username):
    if username is not None:
        user = session.query(UserOrm).filter(
            UserOrm.username == username).first()
    
    if(user is None):
        return False
    
    return UserWithHashModel.from_orm(user)
