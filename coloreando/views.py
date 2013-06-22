from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
import random

class LandingView(TemplateView):
    template_name = "landing.html"

    def get(self, request):
        return super(LandingView, self).get(request)


class LoginView(TemplateView):

    def post(self, request):
    	#Create new canvas
    	new_canvas_name = '-'.join(
    		(request.POST['username'], str(random.randint(1,1000000))))
    	#Save client
    	#Notify all clients of new user
        return redirect('{}#{}'.format(reverse('dashboard_view'), new_canvas_name))


class DashboardView(TemplateView):
	template_name = "dashboard.html"

	def get(self, request):
    	#load current state
		return super(DashboardView, self).get(request)


class DashboardView(TemplateView):
    template_name = "dashboard.html"

