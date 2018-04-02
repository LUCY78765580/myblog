#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User,Say,Post,Link,Tag,Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate=Migrate(app,db)
manager=Manager(app)


#@app.shell_context_processor
def make_shell_context():
	return dict(app=app, db=db, User=User,Say=Say,Post=Post,Link=Link,Tag=Tag,Comment=Comment)


#@app.cli.command()
#@click.option('--length', default=25,help='Number of functions to include in the profiler report.')
#@click.option('--profile-dir', default=None,help='Directory where profiler data files are saved.')
#def profile(length, profile_dir):
#	"""Start the application under the code profiler."""
#	from werkzeug.contrib.profiler import ProfilerMiddleware
#	app.wsgi_app=ProfilerMiddleware(app.wsgi_app, restrictions=[length],profile_dir=profile_dir)
#	app.run()


#@app.cli.command()
#def deploy():
#	"""Run deployment tasks."""
	# migrate database to latest revision
#	upgrade()


@manager.command    
def init_data():
	""" cretat a new user as admin"""
	db.create_all()
	admin_name=os.environ.get('FLASK_ADMIN_NAME')
	admin_email=os.environ.get('FLASK_ADMIN_EMAIL')
	admin_password=os.environ.get('FLASK_ADMIN_PASSWORD')
	user_admin=User(name=admin_name,email=admin_email,password=admin_password)
	db.session.add(user_admin)
	db.session.commit()

@manager.command
def drop_all_data():
	"""drop the database"""
	db.drop_all()


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)


if __name__=='__main__':
	manager.run()


