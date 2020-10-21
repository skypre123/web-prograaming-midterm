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
    name=StringField('제목', validators=[DataRequired()])
    writer=StringField('작성자', validators=[DataRequired()])
    content=TextAreaField('내용', validators=[DataRequired()])
    submit=SubmitField('게시')
    cancel=SubmitField('취소')

@app.route('/writing_page', methods=['GET', 'POST'])
def writingform():
    form=WritingForm()
    if form.validate_on_submit():
        session['name']=form.name.data
        session['writier']=form.writer.data
        session['content']=form.content.data
        return redirect(url_for('boardform'))
    return render_template('writing.html', form=form, name=session.get('name'), writer=session.get('writer'), content=session.get('content'))


class BoardForm(FlaskForm):
    write=SubmitField('작성')

@app.route('/board_page')
def boardform():
    form=BoardForm()
    return render_template('board.html', form=form)


class PostForm(FlaskForm):
    board=SubmitField('게시판')

@app.route('/post_page')
def postform():
    form=PostForm()
    return render_template('post.html', form=form)


class AuthorForm(FlaskForm):
    board=SubmitField('게시판')
    userdelete=SubmitField('작성자 삭제')

@app.route('/author_page')
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
    body=db.Column(db.String)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post%r>' %self.title



if __name__ == '__main__':
    app.run()
