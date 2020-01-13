# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, flash, redirect, url_for, flash, session

from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField, FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import pymysql
#import config     #把上面的配置文件导入进来

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'dev'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/testflask'
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

#app.config.from_object(config)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
manager = Manager(app)

db.create_all()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(5, 20)])
    remember = BooleanField('Remember me')
    submit = SubmitField()

# 主页
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
    # 判断是否已经登陆，如果还没有登陆，退回到登录界面
    username = session.get('username')
    # 如果还没有登录，就返回登录页面
    if username == None:
        return redirect(url_for('login'))
    # 从数据库中获取展示数据
    #data = db.show()
    #return render_template('index.html', all_message=data, user=username)
    return render_template('index.html',  user=username)



@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.debug('A value for debugging')
    form = LoginForm()
    if form.validate_on_submit():
        app.logger.debug('uasername=%s, pwd=%s', form.username.data, form.password.data)
        #code = form['username']
        #api = form['password']
        if form.username.data != 'admin' or form.password.data != 'admin':
            return render_template('login.html', form=form, error="username or pwd is error!")
        else:
            return redirect(url_for('index'))
    return render_template('login.html', form=form, error='')


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    manager.run()


