"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

from unittest import TestCase
from sqlalchemy import exc

from app import app
from models import db, User



# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup('test1', 'test1@email.com', 'password', None)
        u1id = 111
        u1.id = u1id

        u2 = User.signup('test2', 'test2@email.com', 'password', None)
        u2id = 2
        u2.id = u2id

        u1 = User.query.get(u1id)
        u2 = User.query.get(u2id)

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.following), 0)

    def test_user_rep(self):
        self.assertEqual(self.u1.__repr__(), "<User #111: test1, test1@email.com>")


#############################################################################################
# Following Tests

    def test_is_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_followed_by(self):
        self.u2.following.append(self.u1)
        db.session.commit()

        self.assertTrue(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))


################################################################################################
# Test signup

    def test_valid_signup(self):
        test_u = User.signup(
            "testuser", "user@test.com", "password", None)
        uid = 11111
        test_u.id = uid
        db.session.commit()

        test_user = User.query.get(uid)
        self.assertIsNotNone(test_u)
        self.assertEqual(test_u.username, "testuser")
        self.assertEqual(test_u.email, "user@test.com")
        self.assertNotEqual(test_u.password, "password")

    def test_invalid_username_signup(self):
        test_u = User.signup(
            None, "user@test.com", "password", None)
        uid = 22222
        test_u.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_email_signup(self):
        test_u = User.signup(
            "testuser", None, "password", None)
        uid = 22222
        test_u.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup(
            "testuser", "user@test.com", None, None)

#############################################################################################
# Test authentication

    def test_valid_authentication(self):
        self.assertTrue(User.authenticate("test1", 'password'))

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("wrongusername", "password"))

    def test_invalid_password(self):
        self.assertFalse(User.authenticate("test1", "wrongpassword"))
