# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, flash, session

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField, FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length

from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'dev'

bootstrap = Bootstrap(app)


class HelloForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(5, 20)])
    remember = BooleanField('Remember me')
    submit = SubmitField()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def test_form():
    app.logger.debug('A value for debugging')
    form = HelloForm()
    if form.validate_on_submit():
        app.logger.debug('uasername=%s, pwd=%s', form.username.data, form.password.data)
        if form.username.data != 'admin' or form.password.data != 'admin':
            return render_template('form.html', form=form, error="username or pwd is error!")
        else:
            return redirect(url_for('index'))
    return render_template('form.html', form=form, error='')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
