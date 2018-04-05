#-*- coding:utf-8 -*-
from flask import render_template,redirect,request,url_for,flash
from flask_login import current_user
from . import db
from .models import User,Post,Tag,Say,Link
from flask_admin import Admin,BaseView,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView


admin=Admin(
        name='My Blog',
        index_view=AdminIndexView(
        template='index.html',
        name=u'Admin',
        url='/admin'
    ))


class MyBaseView(BaseView):
	def is_accessible(self):
		return current_user.is_authenticated

class NewPostView(MyBaseView):
	@expose('/')
	def new_post(self):
		return redirect(url_for('main.new_post'))

class NewSayView(MyBaseView):
	@expose('/')
	def new_say(self):
		return redirect(url_for('main.new_say'))

class NewLinkView(MyBaseView):
	@expose('/')
	def new_link(self):
		return redirect(url_for('main.new_link'))



class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

class UserView(MyModelView):
	can_create=False
	column_labels={
	'id':'序号',
	'name':'名称',
	'email':'电子邮件',
	'password':'密码',
	}
	column_list=('id','name','email','password')
	def __init__(self,session,**kwargs):
		super(UserView,self).__init__(User,session,**kwargs)


class PostView(MyModelView):
	can_create=False
	column_labels={
    'id':'序号',
    'category':'分类',
	'tag_string':'标签',
    'title':'标题',
    'create_time':'发布时间',
	'view':'浏览',
    'brief':'摘要',
    'content':'文章内容'
    }
	column_list=('id','category','tag_string','title','create_time','view','brief','content')
	def __init__(self,session,**kwargs):
		super(PostView,self).__init__(Post,session,**kwargs)


class SayView(MyModelView):
	can_create=False
	column_labels={
    'id':'序号',
    'create_time':'发布时间',
	'like':'点赞',
    'content':'说说内容'
    }
	column_list=('id','create_time','like','content')
	def __init__(self,session,**kwargs):
		super(SayView,self).__init__(Say,session,**kwargs)

class LinkView(MyModelView):
	can_create=False
	column_labels={
    'id':'序号',
    'create_time':'时间',
    'name':'名称',
    'link':'链接'
    }	
	column_list=('id','create_time','name','link')
	def __init__(self,session,**kwargs):
		super(LinkView,self).__init__(Link,session,**kwargs)


