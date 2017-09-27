#-*- coding:utf-8 -*-
from flask import render_template,redirect,url_for,abort,flash,request,current_app
from flask_login import login_required,current_user
from .forms import SayForm, PostForm,LinkForm
from . import main
from .. import db
from .. import simplemde
from ..models import User,Say,Post,Link,Tag
from datetime import datetime
import markdown


@main.route('/',methods=['GET','POST'])
def home():
	page=request.args.get('page',1,type=int)
	pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('home.html',posts=posts,pagination=pagination)

@main.route('/new_post',methods=['GET','POST'])
@login_required
def new_post():
	form=PostForm()
	if request.method=="POST" and form.validate_on_submit():
		content=form.content.data
		content_html=markdown.markdown(content)
		post=Post(title=form.title.data,category=form.category.data,brief=form.brief.data,content=content,content_html=content_html,timestamp=datetime.now())
		tag_list=form.tag.data.split(',')
		for tag_name in tag_list:
			t=db.session.query(Tag).filter(Tag.name==tag_name).first()
			if not t:
				t=Tag(name=tag_name)
			post.tag.append(t)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('.post',id=post.id,title=post.title))
		flash(u'成功创建文章！')
	return render_template('new_post.html',form=form)

@main.route('/post/<int:id>/<title>',methods=['GET','POST'])
def post(id,title):
	post=Post.query.get_or_404(id)
	post.view+=1
	return render_template('post.html',post=post,title=title)

@main.route('/edit_post/<int:id>/<title>',methods=['GET','POST'])
@login_required
def edit_post(id,title):
	post=Post.query.get_or_404(id)
	form=PostForm()
	if request.method=="POST" and form.validate_on_submit():
		post.title=form.title.data
		post.category=form.category.data
		post.brief=form.brief.data
		post.content=form.content.data
		post.content_html=markdown.markdown(post.content)
		post.timestamp=datetime.now()
		db.session.add(post)
		return redirect(url_for('.post',id=post.id,title=post.title))
		flash(u'成功更新文章！')
	form.title.data=post.title
	form.category.data=post.category
	form.brief.data=post.brief
	form.content.data=post.content
	return render_template('edit_post.html',form=form,post=post)


@main.route('/say',methods=['GET','POST'])
def say():
	page=request.args.get('page',1,type=int)
	pagination=Say.query.order_by(Say.timestamp.desc()).paginate(page,per_page=10,error_out=False)
	says=pagination.items
	return render_template('say.html',says=says,pagination=pagination)

@main.route('/new_say',methods=['GET','POST'])
@login_required
def new_say():
	form=SayForm()
	if request.method=="POST" and form.validate_on_submit():
		say=Say(content=form.content.data,timestamp=datetime.now())
		db.session.add(say)
		db.session.commit()
		return redirect(url_for('.say'))
	return render_template('new_say.html',form=form)


@main.route('/link',methods=['GET','POST'])
def link():
    links=Link.query.order_by(Link.timestamp.asc())
    return render_template('link.html',links=links)

@main.route('/new_link',methods=['GET','POST'])
@login_required
def new_link():
	form=LinkForm()
	if request.method=="POST" and form.validate_on_submit():
		link=Link(name=form.name.data,link=form.link.data,timestamp=datetime.now())
		db.session.add(link)
		db.session.commit()
		return redirect(url_for('.link'))
	return render_template('new_link.html',form=form)


@main.route('/technique')
def technique():
	page=request.args.get('page',1,type=int)
	pagination=Post.query.filter_by(category='technique').order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('technique.html',posts=posts,pagination=pagination)


@main.route('/life')
def life():
	page=request.args.get('page',1,type=int)
	pagination=Post.query.filter_by(category='life').order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('life.html',posts=posts,pagination=pagination)


@main.route('/tag',methods=['GET','POST'])
def tag():	
	tag_list=Tag.query.all()
	if tag_list:
		return render_template('tag.html',tag_list=tag_list)
	else:
		abort(404)
		return render_template('404.html')

@main.route('/tag_detail/<int:id>/<name>',methods=['GET','POST'])
def tag_detail(id,name):
	tag=Tag.query.get_or_404(id)
	page=request.args.get('page',1,type=int)
	pagination=tag.posts.order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('tag_detail.html',tag=tag,name=name,posts=posts,pagination=pagination)	


@main.route('/message')
def message():
	return render_template('message.html')

@main.route('/donate')
def donate():
	return render_template('donate.html')

@main.route('/about')
def about():
	return render_template('about.html')


