import simplejson
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from django.http import HttpResponse
from coloreando.dashboard import get_dashboard, save_event, get_events


def socketio_handle(request):
    socketio_manage(request.environ, {'/coloreando': EventNamespace},
                    request)
    return HttpResponse()


class EventNamespace(BaseNamespace, BroadcastMixin):

    def on_draw(self, event):
        color = event.get('color')
        oldX = event.get('oldX')
        oldY = event.get('oldY')
        newX = event.get('newX')
        newY = event.get('newY')
        dashboard_id = event.get('dashboard_id')
        save_event(color, oldX, oldY, newX, newY, dashboard_id)
        # Send drawing event to all other clients
        self.broadcast_event_not_me('draw_response',
                                    simplejson.dumps({'success': 'true', 'event': event}))

    def on_get_events(self, event):
        dashboard_id = event.get('dashboard_id')
        events = get_events(dashboard_id)
        self.broadcast_event(
            'get_events_response', simplejson.dumps({'events': events}))

    def on_get_buddies(self, event):
        dashboard_id = event.get('dashboard_id')
        dashboard = get_dashboard(dashboard_id)
        buddies = [{
            'username': b.username, 'color_id': b.color_id} for b in dashboard.buddies]
        self.broadcast_event('get_buddies_response', simplejson.dumps(
            {'buddies': buddies}))
