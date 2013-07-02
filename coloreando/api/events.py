from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from django.http import HttpResponse

def socketio_handle(request):
    socketio_manage(request.environ, {'/event': EventNamespace},
                    request)
    return HttpResponse()

class EventNamespace(BaseNamespace):

    def on_draw(self, msg):
        print msg
        self.emit('gotit', 'ok!')
