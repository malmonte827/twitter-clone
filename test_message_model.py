"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

from unittest import TestCase
from sqlalchemy import exc

from app import app, CURR_USER_KEY
from models import db, User, Message, Follows, Likes



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

class MessageModelTestCase(TestCase):
    """Test model for users"""

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 11111
        u = User.signup("test", "test@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        """Does basic model work?"""

        m = Message(
            text="test message",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        self.assertIsNotNone(self.u.messages)
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test message")

    def test_message_likes(self):
        """  """

        m1= Message(
            text="test message1",
            user_id=self.uid
        )

        u = User.signup("testtttt", "testing@test.com", "password", None)   
        uid = 2222
        u.id=uid

        db.session.add_all([u, m1])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()

        self.assertIsNotNone(u.likes)
        self.assertEqual(len(u.likes), 1)
        self.assertEqual(u.likes[0].text, "test message1")


    def test_invalid_text(self):

        m= Message(
            text=None,
            user_id=self.uid
        )

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(m)
            db.session.commit()
        