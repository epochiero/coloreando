from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView


class LandingView(TemplateView):
    template_name = "landing.html"

    def get(self, request):
        return super(LandingView, self).get(request)


class LoginView(TemplateView):

    def post(self, request):
    	#Save client
    	#Notify all clients of new user
        return redirect(reverse('dashboard_view'))


class DashboardView(TemplateView):
	template_name = "dashboard.html"

	def get(self, request):
    	#load current state
		return super(DashboardView, self).get(request)

