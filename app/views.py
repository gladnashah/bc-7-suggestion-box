from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager 
from forms import LoginForm, RegistrationForm, PostForm
from models import User, Post
from flask.ext.wtf import Form
from decorators import admin_required, permission_required



@app.route('/index', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data,
						author=current_user._get_current_object())
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html', form=form, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None:
			login_user(user, form.remember_me.data)
			return  redirect('/index')
		else:
			flash('Invalid email or password.')
	return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data)
		user.hash_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You can now login.')
		return redirect('/login')
	return render_template('register.html', title="Register", form=form)
	

@app.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
	page = request.args.get('page', 1, type=int)
	pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
		error_out=False)
	comments = pagination.items
	return render_template('moderate.html', comments=comments,
							pagination=pagination, page=page)

@app.route('/moderate/enable/<int:id>')
@login_required

def moderate_enable(id):
	comment = Comment.query.get_or_404(id)
	comment.disabled = False
	db.session.add(comment)
	return redirect(url_for('.moderate',
	page=request.args.get('page', 1, type=int)))

@app.route('/moderate/disable/<int:id>')
@login_required

def moderate_disable(id):
	comment = Comment.query.get_or_404(id)
	comment.disabled = True
	db.session.add(comment)
	return redirect(url_for('.moderate',
							page=request.args.get('page', 1, type=int)))

@app.route('/admin')
@login_required
@admin_required
def for_admins_only():
	return "For administrators!"


@app.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
	return "For comment moderators!"


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and \
			not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash('The post has been updated.')
		return redirect(url_for('post', id=post.id))
	form.body.data = post.body
	return render_template('edit_post.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500