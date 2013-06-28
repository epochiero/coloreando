from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

@namespace('/chat')
class EventNamespace(BaseNamespace):
    def on_draw(self, msg):
    	print msg
        self.emit('gotit', 'ok!')