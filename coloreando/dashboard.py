import json
import random
import requests

from django.core.urlresolvers import reverse

from utils import redis_connection
from coloreando.settings import prod as settings

import logging
logger = logging.getLogger(__name__)


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
            slug = username.replace(" ", "-")
            self.dashboard_id = '-'.join((slug, str(random.randint(1, 1000000))))
        self.short_url = None
        self.buddies = []

    def add_buddy(self, buddy):
        self.buddies.append(buddy)

    def save(self):
        redis = redis_connection()
        redis.set(self.dashboard_id, self.to_json())

    def to_json(self):
        self.short_url = self.get_short_url()
        doc = {"dashboard_id": self.dashboard_id}
        doc["buddies"] = [buddy.to_json() for buddy in self.buddies]
        doc["short_url"] = self.short_url
        return json.dumps(doc)

    def get_short_url(self):
        if not self.short_url:
            long_url = "{}{}".format(settings.BASE_URL, self.get_absolute_url())
            r = requests.post("https://api-ssl.bitly.com/v3/shorten", {"longUrl": long_url, "access_token": settings.BITLY_ACCESS_TOKEN})
            self.short_url = r.json()['data']['url']
        return self.short_url

    def get_absolute_url(self):
        return reverse('dashboard_view', args=(self.dashboard_id,))


def get_dashboard(dashboard_id):
    redis = redis_connection()
    dashboard = Dashboard(dashboard_id)
    dashboard_json = json.loads(redis.get(dashboard_id))
    for buddy in dashboard_json['buddies']:
        dashboard.add_buddy(Buddy(buddy["username"], buddy["color_id"]))
    dashboard.short_url = dashboard_json["short_url"]
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
