#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User,Say,Post,Link,Tag,Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate=Migrate(app,db)


#@app.shell_context_processor
def make_shell_context():
	return dict(app=app, db=db, User=User,Say=Say,Post=Post,Link=Link,Tag=Tag,Comment=Comment)

#def profile(length, profile_dir):
#	"""Start the application under the code profiler."""
#	from werkzeug.contrib.profiler import ProfilerMiddleware
#	app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],profile_dir=profile_dir)
#	app.run()

#@app.cli.command()
#def deploy():
#	"""Run deployment tasks."""
#	# migrate database to latest revision
#	upgrade()


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)


if __name__=='__main__':
	manager.run()


