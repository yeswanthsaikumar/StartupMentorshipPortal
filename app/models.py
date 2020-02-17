from datetime import datetime
from app import db , login , app
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt

@login.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.user_id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.user_id'))
)

class User( UserMixin, db.Model):
	__tablename__ = 'user'

	user_id = db.Column(db.Integer , primary_key=True)
	username = db.Column(db.String(64) ,index=True , unique=True)
	email = db.Column(db.String(64) , index=True , unique=True)
	password_hash = db.Column(db.String(200))
	about_me = db.Column(db.String(200))
	last_seen = db.Column(db.DateTime , default=datetime.utcnow)
	user_category = db.Column(db.String(50) ,default=None)
	sector = db.Column(db.String(50) , default=None)
	posts = db.relationship('Post' , backref='author' , lazy='dynamic')
	stories = db.relationship('Stories' , backref='author' , lazy='dynamic')
	messages_sent = db.relationship('Message' , backref='author', foreign_keys='Message.sender_id' ,lazy='dynamic')
	messages_recieved = db.relationship('Message' , backref='recipient' ,foreign_keys='Message.recipient_id' , lazy='dynamic')
	last_message_read_time = db.Column(db.DateTime)
	followed = db.relationship(
	'User', secondary=followers,
	primaryjoin=(followers.c.follower_id == user_id),
	secondaryjoin=(followers.c.followed_id == user_id),
	backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


	def __repr__(self):
		return self.username

	def get_id(self):
		return (self.user_id)

	def set_password(self , password):
		self.password_hash = generate_password_hash(password)


	def check_password(self , password):
		return check_password_hash(self.password_hash , password )


	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


	def follow(self , user) :
		if not self.is_following(user) :
			self.followed.append(user)


	def unfollow(self , user) :
		if self.is_following(user) :
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.user_id ).count() > 0

	def followed_posts(self):
		followed =  Post.query.join(
			followers,(followers.c.followed_id == Post.user_id)).filter(
			followers.c.follower_id == self.user_id)

		own = Post.query.filter_by( user_id = self.user_id)

		return followed.union(own).order_by(Post.timeStamp.desc())
			
	def new_messages(self):
		last_read_time = self.last_message_read_time or datetime(2000 , 1 , 1)
		return Message.query.filter_by().filter( Message.timestamp > last_read_time ).count()

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.user_id, 'exp': time() + expires_in},
			app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			user_id = jwt.decode(token, app.config['SECRET_KEY'],
							algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(user_id)


class Post(db.Model):
	__tablename__ = 'post'

	Post_id = db.Column( db.Integer, primary_key=True)
	body = db.Column(db.Text(4294967295))
	timeStamp = db.Column(db.DateTime , index=True , default=datetime.utcnow)
	user_id = db.Column(db.Integer , db.ForeignKey('user.user_id'))

	def __repr__(self):
		return '<Post : {}>'.format(self.body)


class Stories(db.Model):
	__tablename__ = 'stories'

	stories_id = db.Column( db.Integer, primary_key=True)
	body = db.Column(db.Text(4294967295))
	timeStamp = db.Column(db.DateTime , index=True , default=datetime.utcnow)
	user_id = db.Column(db.Integer , db.ForeignKey('user.user_id'))

	def __repr__(self):
		return '<Story : {}>'.format(self.body)

class News(db.Model):
	__tablename__ = 'news'

	news_id = db.Column( db.Integer, primary_key=True)
	body = db.Column(db.Text(4294967295))
	timeStamp = db.Column(db.DateTime , index=True , default=datetime.utcnow)
	sector = db.Column(db.String(30))

	def __repr__(self):
		return '<Post : {}>'.format(self.body)


class Message(db.Model):
	__tablename__= 'message'

	message_id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	recipient_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	body = db.Column(db.String(140))
	timeStamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return '<Message {}>'.format(self.body)


