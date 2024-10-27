"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, Message, User, Likes, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewsTestCase(TestCase):
    """ Test Views for Users"""


    def setUp(self):
        """Create test client and sampe data"""

        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    ############################################################    test user
        
        self.testuser = User.signup("testuser", "test@test.com", "password", None)
        self.testuser.id = 12345

    
    ############################################################    extra users
        
        self.u1 = User.signup("user1", "user1@test.com", "password", None)
        self.u1.id = 11111

        self.u2 = User.signup("user2", "user2@test.com", "password", None)
        self.u2.id = 22222

        self.u3 = User.signup("user3", "user3@test.com", "password", None)
        self.u3.id = 33333

        db.session.commit()

        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_show_users(self):
        with self.client as c:
            res = c.get('/users')

            self.assertEqual(res.status_code, 200)
            self.assertIn("@user1", str(res.data))
            self.assertIn("@user2", str(res.data))
            self.assertIn("@user3", str(res.data))

    def test_user_search(self):
        with self.client as c:
            res = c.get('/users?q=user1')

            self.assertEqual(res.status_code, 200)
            self.assertIn('@user1', str(res.data))
            self.assertNotIn('@user3', str(res.data))
            self.assertNotIn('@user2', str(res.data))
            self.assertNotIn('@testuser', str(res.data))

    def test_show_user(self):
        with self.client as c:
            res = c.get(f'/users/{self.testuser.id}')

            self.assertEqual(res.status_code, 200)
            self.assertIn('@testuser', str(res.data))
            self.assertNotIn('@user1', str(res.data))
            self.assertNotIn('@user3', str(res.data))
            self.assertNotIn('@user2', str(res.data))

    def test_show_invalid_user(self):
        with self.client as c:

            res = c.get('users/99999')#<------- not valid user id

            self.assertEqual(res.status_code, 404)
            self.assertNotIn('@9999', str(res.data))

    def setup_followers(self):
        f1= Follows(user_being_followed_id=self.u1.id, user_following_id=self.testuser.id) 
        f2= Follows(user_being_followed_id=self.u2.id, user_following_id=self.testuser.id)
        f3 = Follows(user_being_followed_id=self.testuser.id, user_following_id=self.u1.id)
        f4 = Follows(user_being_followed_id=self.testuser.id, user_following_id=self.u2.id)
        
        db.session.add_all([f1,f2,f3,f4])
        db.session.commit()

    def test_show_following(self):
        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            res = c.get(f'/users/{self.testuser.id}/following')
            self.assertEqual(res.status_code, 200)
            self.assertIn('@user1', str(res.data))
            self.assertIn('@user2', str(res.data))
            self.assertNotIn('@user3', str(res.data))

    def test_unauthorized_show_following(self):
        with self.client as c:
            
            res = c.get(f'/users/{self.testuser.id}/followers', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Access unauthorized', str(res.data))
            self.assertNotIn('@user1', str(res.data))

    def test_show_followers(self):
        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            res = c.get(f'/users/{self.testuser.id}/following')
            self.assertEqual(res.status_code, 200)
            self.assertIn('@user1', str(res.data))
            self.assertIn('@user2', str(res.data))
            self.assertNotIn('@user3', str(res.data))

    def test_unauthorized_show_followers(self):
        with self.client as c:
        
            res = c.get(f'/users/{self.testuser.id}/followers', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Access unauthorized', str(res.data))
            self.assertNotIn('/@user1', str(res.data))

    def test_add_follow(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                
            u = User.signup("testtest", "testtest@test.com", "password", None)
            u.id = 3333
            db.session.commit()
            
            
            res = c.post(f'/users/follow/{u.id}', follow_redirects=True)


            f = Follows.query.filter(Follows.user_following_id == self.testuser.id ).all()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(f), 1)
            self.assertEqual(f[0].user_following_id, self.testuser.id)

    def test_add_like(self):
        m = Message(id=9876, text="testingggggg", user_id=self.u2.id)
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            res = c.post('/users/add_like/9876', follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            l = Likes.query.filter(Likes.message_id == 9876).all()
            self.assertEqual(len(l), 1)
            self.assertEqual(l[0].user_id, self.testuser.id)

    def test_remove_like(self):
        m = Message(id=4545, text="test like", user_id=self.u1.id)
        db.session.add(m)
        db.session.commit()

        l = Likes(user_id=self.testuser.id, message_id=4545)
        db.session.add(l)
        db.session.commit()

        with self.client as c:
            
            res = c.post(f'/users/remove_like/{m.id}', follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            likes= Likes.query.filter(Likes.message_id == m.id).all()
            self.assertEqual(len(likes), 1)

    def test_unauthorized_like(self):
        m = Message(id=5656, text="testtttt", user_id=self.testuser.id)

        with self.client as c:
            res = c.post(f'/users/add_like/{m.id}', follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            self.assertIn("Access unauthorized", str(res.data))






