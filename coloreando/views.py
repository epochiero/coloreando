from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView


class LandingView(TemplateView):
    template_name = "landing.html"

    def get(self, request):
        return super(LandingView, self).get(request)


class LoginView(TemplateView):

    def post(self, request):
    	#
        return super(LandingView, self).post(request)


class DashboardView(TemplateView):
    template_name = "dashboard.html"

