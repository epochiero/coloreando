import random
from utils import redis_connection


class Buddy(object):
	"""
    Main Buddy object.
    """
    def __init__(self, username, color_id):
        self.username = username
        self.color_id = color_id


class Canvas(object):
    """
    Main Canvas object.
    """
    def __init__(self, username):
        self.canvas_id = '-'.join((username, str(random.randint(1, 1000000))))
        self.buddies = []

    def add_buddy(self, buddy):
        self.buddies.append(buddy)

    def save(self):
        conn = redis_connection()
   		conn.
