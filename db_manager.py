from app import db, User, Post

if __name__=='__main__':
    db.create_all()
    db.session.commit()

    print(User.query.all())