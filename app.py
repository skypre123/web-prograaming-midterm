from flask import Flask, redirect, request, make_response, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

basedir=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY']='hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

@app.route('/user/<name>')
def user_bootstrap(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


class WritingForm(FlaskForm):
    title=StringField('제목', validators=[DataRequired()])
    name=StringField('작성자', validators=[DataRequired()])
    body=TextAreaField('내용', validators=[DataRequired()])
    submit=SubmitField('게시')
    cancel=SubmitField('취소')

@app.route('/writing', methods=['GET', 'POST'])
def writingform():
    form=WritingForm()
    if form.validate_on_submit():
        user=User(name=form.name.data)
        title=Post(title=form.title.data)
        body=Post(body=form.body.data)
        db.session.add(user)
        db.session.add(title)
        db.session.add(body)

        session['title']=form.title.data
        session['name']=form.name.data
        session['body']=form.body.data
        db.session.commit()

        form.name.data = ''
        return redirect(url_for('boardform'))
    return render_template('writing.html', form=form, title=session.get('title'), name=session.get('name'), body=session.get('body'))


class BoardForm(FlaskForm):
    write=SubmitField('작성')

@app.route('/board', methods=['GET', 'POST'])
def boardform():
    form=BoardForm()
    if form.validate_on_submit():
        session['write']=form.write.data
        return redirect(url_for('writingform'))
    return render_template('board.html', form=form, write=session.get('write'))


class PostForm(FlaskForm):
    board=SubmitField('게시판')

@app.route('/post')
def postform():
    form=PostForm()
    return render_template('post.html', form=form)


class AuthorForm(FlaskForm):
    board=SubmitField('게시판')
    userdelete=SubmitField('작성자 삭제')

@app.route('/author')
def authorform():
    form=AuthorForm()
    return render_template('author.html', form=form)









class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True)
    posts=db.relationship('Post', backref='user')

    def __repr__(self):
        return '<User%r>' %self.name

class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(64), unique=True,)
    body=db.Column(db.Text)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post%r>' %self.title



if __name__ == '__main__':
    app.run()
