from flask.ext.script import Manager
from tracker.app import app
import rethinkdb as r


manager = Manager(app)

@manager.command
def createdb():
	conn = r.connect()

	conn.run(r.db_create("tracker"))
	conn.run(r.db("tracker").table_create("torrents"))
	conn.run(r.db("tracker").table_create("users"))

	conn.close()
	print "Database Created"


@manager.command
def dropdb():
	conn = r.connect()

	conn.run(r.db_drop("tracker"))

	conn.close()
	print "Database Dropped"

if __name__ == "__main__":
	manager.run()