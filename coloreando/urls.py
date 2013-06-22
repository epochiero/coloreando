from django.conf.urls import patterns, include, url
from views import LandingView, LoginView

urlpatterns = patterns('',
    url('^$', LandingView.as_view(), name='landing_view'),
    url('^login$', LoginView.as_view(), name='login_view'),
    url('^dashboard$', DashboardView.as_view(), name='dashboard_view'),
)
