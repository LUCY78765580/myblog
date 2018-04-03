#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User,Say,Post,Link,Tag,Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate=Migrate(app,db)
manager=Manager(app)


def make_shell_context():
	return dict(app=app, db=db, User=User,Say=Say,Post=Post,Link=Link,Tag=Tag,Comment=Comment)


@app.cli.command()
def deploy():
	"""Run deployment tasks."""
	upgrade()
	admin_name=os.environ.get('FLASK_ADMIN_NAME')
	admin_email=os.environ.get('FLASK_ADMIN_EMAIL')
	admin_password=os.environ.get('FLASK_ADMIN_PASSWORD')
	user_admin=User(name=admin_name,email=admin_email,password=admin_password)
	db.session.add(user_admin)
	db.session.commit()


#manager.add_command('shell', Shell(make_context=make_shell_context))
#manager.add_command('db',MigrateCommand)

if __name__=='__main__':
	manager.run()


