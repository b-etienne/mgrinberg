import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Posts
from datetime import datetime, timedelta

#

class TestCase(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CRSF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()


	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_avatar(self):
		user = User(pseudo='john', email='john@example.com')
		avatar = user.avatar(128)
		expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
		assert(avatar[:len(expected)] == expected)


	def test_user_unique(self):
		x = User(pseudo="XXX", email="xxx@xxx.fr")
		db.session.add(x)
		db.session.commit()
		x = User(pseudo="XXX", email="xxx@xxx.fr")
		assert(x.pseudo_exists(x.pseudo))


	def test_follow(self):
		u1 = User(pseudo="XXX", email="xxx@xxx.fr")
		u2 = User(pseudo="YYY", email="yyy@yyy.fr")
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		assert(u1.unfollow(u2) is None)
		assert(u2.unfollow(u1) is None)
		u = u1.follow(u2)
		assert(u is not None)
		db.session.add(u)
		db.session.commit()
		assert(u1.is_following(u2))
		assert(u1.follow(u2) is None)
		assert(u1.follows.count()==1)
		assert(u1.follows.first().pseudo == "YYY")
		assert(u2.followers.count()==1)
		assert(u2.followers.first().pseudo == "XXX")
		u = u1.unfollow(u2)
		assert(u is not None)
		db.session.add(u)
		db.session.commit()	
		assert(u1.is_following(u2) is False)
		assert(u1.follows.count()==0)
		assert(u2.followers.count()==0)


	def test_follow_posts(self):
		# Users
		u1 = User(pseudo="john", email="john@xxx.fr")
		u2 = User(pseudo="marie", email="marie@yyy.fr")
		u3 = User(pseudo="david", email="david@xxx.fr")
		u4 = User(pseudo="bob", email="bob@yyy.fr")
		db.session.add(u1)
		db.session.add(u2)
		db.session.add(u3)
		db.session.add(u4)

		# Posts
		now = datetime.utcnow()
		p1 = Posts(body="Post from John", author=u1, datestamp=now+timedelta(1))
		p2 = Posts(body="Post from Marie", author=u2, datestamp=now+timedelta(2))
		p3 = Posts(body="Post from David", author=u3, datestamp=now+timedelta(3))
		p4 = Posts(body="Post from Bob", author=u4, datestamp=now+timedelta(4))
		db.session.add(p1)
		db.session.add(p2)
		db.session.add(p3)
		db.session.add(p4)
		db.session.commit()

		# Followers
		u1.follow(u1).follow(u2).follow(u4)
		u2.follow(u2).follow(u3)
		u3.follow(u3).follow(u4)
		u4.follow(u4)
		assert(u1.is_following(u1))
		assert(u1.is_following(u2))
		assert(u1.is_following(u4))
		db.session.commit()

		r1 = u1.followed_posts().all()
		r2 = u2.followed_posts().all()
		r3 = u3.followed_posts().all()
		r4 = u4.followed_posts().all()

		assert(len(r1) == 3)
		assert(len(r2) == 2)
		assert(len(r3) == 2)
		assert(len(r4) == 1)
		assert(r1 == [p4, p2, p1])
		assert(r2 == [p3, p2])
		assert(r3 == [p4, p3])
		assert(r4 == [p4])

		




if __name__ ==	"__main__":
	unittest.main()
