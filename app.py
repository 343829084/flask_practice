# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, flash, session

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField, FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length

from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'dev'

bootstrap = Bootstrap(app)


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
    app.run(debug=True, host='0.0.0.0')
