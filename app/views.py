from flask import render_template, session, redirect, url_for, request,g, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, RegistrationForm, PostForm
from models import User


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
  
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('login.html')
# def index():
# 	if request.method == 'POST':
# 		form = PostForm()
# 		if form.validate_on_submit():
# 			post = Post (body=form.body.data,
# 						author=current_user._get_current_object())
# 			db.session.add(post)
# 			return redirect(url_for('.index'))
# 		posts = Post.query.order_by(Post.timestamp.desc()).all()
# 		return render_template('index.html', form=form, posts=posts)

@app.route('/posts')
def suggestion():
	return render_template('posts.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			if user is not None and user.verify_password(form.password.data):
				login_user(user, form.remember_me.data)
				return  url_for('/posts')
			flash('Invalid email or password.')
	return render_template('login.html', form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		flash('You can now login.')
		return redirect(url_for('/login'))
	return render_template('register.html', form=form)