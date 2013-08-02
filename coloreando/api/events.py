import simplejson
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin, RoomsMixin
from socketio.namespace import BaseNamespace
from django.http import HttpResponse
from coloreando.dashboard import get_dashboard, save_event, get_events


def socketio_handle(request):
    socketio_manage(request.environ, {'/coloreando': EventNamespace},
                    request)
    return HttpResponse()


class EventNamespace(BaseNamespace, BroadcastMixin, RoomsMixin):

    def on_join_dashboard(self, data):
        self.dashboard_id = data.get('dashboard_id')
        self.join(self.dashboard_id)
        return True

    def on_draw(self, event):
        color = event.get('color')
        size = event.get('size')
        shapeType = event.get('shapeType')
        oldX = event.get('oldX')
        oldY = event.get('oldY')
        newX = event.get('newX')
        newY = event.get('newY')
        dashboard_id = event.get('dashboard_id')
        save_event(color, size, shapeType, oldX, oldY, newX, newY, dashboard_id)

        # Send drawing event to all other clients
        self.emit_to_room(self.dashboard_id, 'draw_response',
                          simplejson.dumps({'success': 'true', 'event': event}))
        return True

    def on_get_events(self, event):
        dashboard_id = event.get('dashboard_id')
        events = get_events(dashboard_id)
        self.emit(
            'get_events_response', {'events': events})

    def on_get_buddies(self, event):
        dashboard_id = event.get('dashboard_id')
        dashboard = get_dashboard(dashboard_id)
        buddies = [{
            'username': b.username, 'color_id': b.color_id} for b in dashboard.buddies]
        self.emit('get_buddies_response', simplejson.dumps(
            {'buddies': buddies}))
