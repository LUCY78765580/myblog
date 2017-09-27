#-*- coding:utf-8 -*-
from . import db,login_manager
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
import time
from datetime import datetime



class User(UserMixin,db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String(64),unique=True,index=True)
	password_hash=db.Column(db.String(128))
	says=db.relationship('Say',backref='writer',lazy='dynamic')
	posts=db.relationship('Post',backref='author',lazy='dynamic')


	def __repr__(self):
		return '<User %r>' %self.email
	
	@property
	def password(self):
		raise AttributeError('password is not a readable atribute')

	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)
	
	
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
	def can(self,permissions):
		return False
	def is_administrator(self):
		return False
login_manager.anonymous_user=AnonymousUser



class Say(db.Model):
	__tablename__='says'
	id=db.Column(db.Integer,primary_key=True)
	content=db.Column(db.Text)
	timestamp=db.Column(db.DateTime,default=datetime.now(),index=True)
	writer_id=db.Column(db.Integer,db.ForeignKey('users.id'))
	like=db.Column(db.Integer,default=0)

	def formatDate(self):
		str=self.timestamp.strftime('%Y-%m-%d')
		return str

	def formatTime(self):
		str=self.timestamp.strftime('%H:%M')
		return str



tag_post=db.Table('tag_post',
		db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
		db.Column('post_id',db.Integer,db.ForeignKey('posts.id')))

class Post(db.Model):
	__tablename__='posts'
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(150))
	brief=db.Column(db.String(250))
	content=db.Column(db.Text)
	content_html=db.Column(db.Text)
	timestamp=db.Column(db.DateTime,default=datetime.now(),index=True)
	category=db.Column(db.String(64),index=True)	
	author_id=db.Column(db.Integer,db.ForeignKey('users.id'))
	tag=db.relationship('Tag',secondary=tag_post,
			backref=db.backref('posts',lazy='dynamic'),lazy='dynamic')
	view=db.Column(db.Integer,default=0)
	like=db.Column(db.Integer,default=0)		


	def __repr__(self):
		return '<Post %r>'%self.title	

	def formatDateTime(self):
		str=self.timestamp.strftime('%Y-%m-%d %H:%M')
		return str


class Link(db.Model):
	__tablename__='links'
	id=db.Column(db.Integer,primary_key=True)
	link=db.Column(db.Text)
	name=db.Column(db.String)
	timestamp=db.Column(db.DateTime,default=datetime.now())

	def __repr__(self):
		return '<Link %r>'%link


class Tag(db.Model):
	__tablename__='tags'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String,unique=True,index=True)

	
