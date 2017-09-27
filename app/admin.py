#-*- coding:utf-8 -*-
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_required,current_user
from . import db
from .models import User,Post,Say,Link
from flask_admin import Admin,BaseView,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView


admin=Admin(
        name='My Blog',
        index_view=AdminIndexView(
        template='index.html',
        name=u'首頁',
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

class PostView(MyModelView):
	can_create=False
	column_labels={
    'id':u'序号',
    'category':u'分类',
    'title':u'标题',
    'timestamp':u'发布时间',
    'brief':u'摘要',
    'content':u'文章内容'
    }
	column_list=('id','category','title','timestamp','brief','content')
	def __init__(self,session,**kwargs):
		super(PostView,self).__init__(Post,session,**kwargs)

class SayView(MyModelView):
	can_create=False
	column_labels={
    'id':u'序号',
    'timestamp':u'发布时间',
    'content':u'说说内容'
    }
	column_list=('id','timestamp','content')
	def __init__(self,session,**kwargs):
		super(SayView,self).__init__(Say,session,**kwargs)

class LinkView(MyModelView):
	can_create=False
	column_labels={
    'id':u'序号',
    'timestamp':u'时间',
    'name':u'名称',
    'link':u'链接'
    }	
	column_list=('id','timestamp','name','link')
	def __init__(self,session,**kwargs):
		super(LinkView,self).__init__(Link,session,**kwargs)




