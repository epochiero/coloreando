from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView

from dashboard import Dashboard, Buddy, get_dashboard
import random
import logging

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
        	dashboard_id = dashboard.dashboard_id
        dashboard.add_buddy(Buddy(username, color_id))
    	dashboard.save()

        request.session["color_id"] = color_id
        #Notify all clients of new user
        return redirect(reverse('dashboard_view', args=(dashboard_id,)))


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, *args, **kwargs):
    	context = super(DashboardView, self).get_context_data(*args, **kwargs)
    	dashboard_id = context['dashboard_id']
    	if dashboard_id:
    		dashboard = get_dashboard(dashboard_id).to_json()
    		context.update(
    			{'dashboard': dashboard,
    			 'color_id': self.request.session.get("color_id"),
    			}
    		)
    		
    	return context

    def get(self, request, *args, **kwargs):
        #load current state
        return super(DashboardView, self).get(request, *args, **kwargs)
