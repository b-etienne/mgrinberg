import os
import unittest

from config import basedir
from app import app, db
from app.models import User


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



if __name__ ==	"__main__":
	unittest.main()
