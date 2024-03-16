from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, NewPlayerForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nate'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login Requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup')
def signup():
    form = NewPlayerForm()
    if form.validate_on_submit():
        flash('Sign Up Requested for user {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=form)