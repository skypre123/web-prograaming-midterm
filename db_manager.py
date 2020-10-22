from app import db, User, Post

if __name__=='__main__':
    db.drop_all()
    db.create_all()
    user_sikyung = User(name='Sikyung')
    user_youngjung=User(name='Youngjung')
    post_skysky=Post(title='skysky', body='skyskysky', user=user_sikyung)
    post_jyjy=Post(title='yjyj', body='jyujyu', user=user_youngjung)

    db.session.add_all([user_sikyung, user_youngjung, post_skysky, post_jyjy])
    db.session.commit()

    print(User.query.all())
    print(Post.query.all())
