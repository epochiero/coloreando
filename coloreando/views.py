import logging
import random

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView

from dashboard import Dashboard, Buddy, get_dashboard

logger = logging.getLogger(__name__)


class LandingView(TemplateView):
    template_name = "landing.html"

    def get(self, request):
        return super(LandingView, self).get(request)


class LoginView(TemplateView):

    def post(self, request):
        #Create new canvas
        username = request.POST['username']
        color_id = request.POST['color_id']
        dashboard_id = request.POST.get('dashboard_id', None)
        if not dashboard_id:
            dashboard = Dashboard(username)
            dashboard_id = dashboard.dashboard_id
        else:
            dashboard = get_dashboard(dashboard_id)
            if dashboard:
            	dashboard_id = dashboard.dashboard_id
            else:
            	dashboard = Dashboard(username)
                dashboard_id = dashboard.dashboard_id
        dashboard.add_buddy(Buddy(username, color_id))
        dashboard.save()

        request.session["color_id"] = color_id
        return redirect(dashboard.get_absolute_url())


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        dashboard_id = context['dashboard_id']
        if dashboard_id:
            dashboard = get_dashboard(dashboard_id)
            context.update(
                {'dashboard': dashboard,
                'short_url': dashboard.short_url,
                'color_id': self.request.session.get("color_id")
                }
            )

        return context

    def get(self, request, *args, **kwargs):
        if not request.session.get("color_id", None):
            # Redirect to login
            return redirect(reverse('landing_view') + '?dashboard_id=' + kwargs['dashboard_id'])
        return super(DashboardView, self).get(request, *args, **kwargs)

