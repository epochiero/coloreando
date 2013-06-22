import json
import random
from utils import redis_connection


class Buddy(object):
    """
    Main Buddy object.
    """
    def __init__(self, username, color_id):
        self.username = username
        self.color_id = color_id

    def to_json(self):
        return {"username": self.username, "color_id": self.color_id}


class Dashboard(object):
    """
    Main Dashboard object.
    """
    def __init__(self, username=None):
        if username:
            self.dashboard_id = '-'.join((username, str(random.randint(1, 1000000))))
        self.buddies = []

    def add_buddy(self, buddy):
        self.buddies.append(buddy)

    def save(self):
        redis = redis_connection()
        redis.set(self.dashboard_id, self.to_json())

    def to_json(self):
        doc = {"dashboard_id": self.dashboard_id}
        doc["buddies"] = [buddy.to_json() for buddy in self.buddies]
        return json.dumps(doc)


def get_dashboard(dashboard_id):
    redis = redis_connection()
    dashboard_value = redis.get(dashboard_id)
    if not dashboard_value:
        return
    dashboard_json = json.loads(redis.get(dashboard_id))
    dashboard = Dashboard()
    dashboard.dashboard_id = dashboard_json["dashboard_id"]
    for buddy in dashboard_json['buddies']:
        dashboard.add_buddy(Buddy(buddy["username"], buddy["color_id"]))
    return dashboard


def save_event(color, oldX, oldY, newX, newY, dashboard_id):
    redis = redis_connection()
    key_name = '{}-events'.format(dashboard_id)
    redis.rpush(key_name, json.dumps({'color': color, 'oldX': oldX, 'oldY': oldY, 'newX': newX, 'newY': newY}))


def get_events(dashboard_id):
    redis = redis_connection()
    key_name = '{}-events'.format(dashboard_id)
    events = redis.lrange(key_name, 0, -1)
    return events
