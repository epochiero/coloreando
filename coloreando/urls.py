from django.conf.urls import patterns, include, url
from views import LandingView, LoginView, DashboardView, SaveEventView, GetEventsView, GetBuddiesView
import socketio.sdjango
from api.events import socketio_handle


urlpatterns = patterns('',
    url('^$', LandingView.as_view(), name='landing_view'),
    url('^login$', LoginView.as_view(), name='login_view'),
    url('^dashboard/(?P<dashboard_id>[a-zA-Z0-9\-]+)$', DashboardView.as_view(), name='dashboard_view'),
    url('^api/saveEvent$', SaveEventView.as_view(), name='save_event_view'),
    url('^api/getEvents$', GetEventsView.as_view(), name='get_events_view'),
    url('^api/getBuddies$', GetBuddiesView.as_view(), name='get_buddies_view'),
    url("^socket\.io", socketio_handle),
)
