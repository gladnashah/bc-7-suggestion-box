from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
from flask.ext.login import UserMixin, AnonymousUserMixin
from datetime import datetime



class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password= db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	comments = db.relationship('Comment', backref='author', lazy='dynamic')
	#roles = db.relationship('User', backref='role', lazy='dynamic')
	

	
	@property
	def is_active(self):
		return True
	
	@property
	def is_authenticated(self):
		return True

	def hash_password(self,password):
		self.password = generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password, password)


	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)
	def __repr__(self):
		return '<User %r>' %(self.username)

# 	def can(self, permissions):
# 		return self.role is not None and \
# 			(self.role.permissions & permissions) == permissions


# 	def is_administrator(self):
# 		return self.can(Permission.ADMINISTER)

# class AnonymousUser(AnonymousUserMixin):
# 	def can(self, permissions):
# 		return False

# 	def is_administrator(self):
# 		return False
# login_manager.anonymous_user = AnonymousUser


	

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	body= db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	comments = db.relationship('Comment', backref='post', lazy='dynamic')


	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
						'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
						'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
				markdown(value, output_format='html'),
				tags=allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)

def __repr__(self):
	return '<Post %r>' % (self.body_html)

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	disabled = db.Column(db.Boolean)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
						'strong']
		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags, strip=True))
db.event.listen(Comment.body, 'set', Comment.on_changed_body)

def __repr__(self):
	return '<Comment %r>' % (self.body)

class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTER = 0x80

# class Role(db.Model):
# 	__tablename__ = 'roles'
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(64), unique=True)
# 	default = db.Column(db.Boolean, default=False, index=True)
# 	permissions = db.Column(db.Integer)
# 	users = db.relationship('User', backref='role', lazy='dynamic')
	



# 	@staticmethod
# 	def insert_roles():
# 		roles = {
# 		'User': (Permission.COMMENT |
# 				Permission.WRITE_ARTICLES, True),
# 		'Moderator': (Permission.COMMENT |
# 					Permission.WRITE_ARTICLES |
# 					Permission.MODERATE_COMMENTS, False),
# 		'Administrator': (0xff, False)
# 		}
# 		for r in roles:
# 			role = Role.query.filter_by(name=r).first()
# 			if role is None:
# 				role = Role(name=r)
# 			role.permissions = roles[r][0]
# 			role.default = roles[r][1]
# 			db.session.add(role)
# 		db.session.commit()

# 	def __repr__(self):
# 		return '<Role %r>' % (self.id)



	

# 	def can(self, permissions):
# 		return self.role is not None and \
# 			(self.role.permissions & permissions) == permissions

# 	def is_administrator(self):
# 		return self.can(Permission.ADMINISTER)

# class AnonymousUser(AnonymousUserMixin):
# 	def can(self, permissions):
# 		return False

# 	def is_administrator(self):
# 		return False
# login_manager.anonymous_user = AnonymousUser





