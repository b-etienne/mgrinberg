from app import db
from flask_login import UserMixin
from hashlib import md5


followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.iid')),
	db.Column('follows_id', db.Integer, db.ForeignKey('user.iid')))


class User(db.Model):

	iid = db.Column(db.Integer, primary_key=True)
	pseudo = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(128), index=True, unique=True)
	posts = db.relationship('Posts', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(256))
	last_seen = db.Column(db.DateTime)
	follows = db.relationship('User',
							  secondary=followers,
							  primaryjoin=(followers.c.follower_id == iid),
							  secondaryjoin=(followers.c.follows_id == iid),
							  backref=db.backref('followers', lazy='dynamic'),
							  lazy='dynamic')

	def __init__(self, pseudo, email):
		self.pseudo = pseudo
		self.email = email


	def __repr__(self):
		return('<User {}>'.format(self.pseudo)) 


	def is_authenticated(self):
		return(True)


	def is_active(self):
		return(True)


	def is_anonymous(self):
		return(False)


	def get_id(self):
		return(str(self.iid))


	def avatar(self, size):
		return('http://www.gravatar.com/avatar/{}?d=mm&s={}'.format(md5(self.email.encode('utf-8')).hexdigest(), size))


	@staticmethod
	def pseudo_exists(pseudo):
		if User.query.filter_by(pseudo=pseudo).first() is not None:
			return True
		return False


	def is_following(self, user):
		return(self.follows.filter(followers.c.follows_id == user.iid).count()>0)
		

	def follow(self, user):
		if not self.is_following(user):
			self.follows.append(user)
			return(self)


	def unfollow(self, user):
		if self.is_following(user):
			self.follows.remove(user)
			return(self)


	def followed_posts(self):
		s = Posts.query.join(followers, (followers.c.follows_id==Posts.user_id))
		s = s.filter(followers.c.follower_id==self.iid)
		s = s.order_by(Posts.datestamp.desc())
		return(s)


class Posts(db.Model):
	iid = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	datestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.iid'))

	def __init__(self, body, author, datestamp):
		self.body = body
		self.user_id = author
		self.datestamp = datestamp

	def __repr__(self):
		return('<Post {}>'.format(self.body))



