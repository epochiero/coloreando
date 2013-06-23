from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView

from dashboard import Dashboard, Buddy, get_dashboard, save_event, get_events
import json
import random


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
        #Notify all clients of new user
        return redirect(reverse('dashboard_view', args=(dashboard_id,)))


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        dashboard_id = context['dashboard_id']
        if dashboard_id:
            dashboard = get_dashboard(dashboard_id)
            context.update(
                {'dashboard': dashboard,
                 'color_id': self.request.session.get("color_id"),
                 }
            )

        return context

    def get(self, request, *args, **kwargs):
        if not request.session.get("color_id", None):
            #Redirect to login
            return redirect(reverse('landing_view') + '?dashboard_id=' + kwargs['dashboard_id'])
        return super(DashboardView, self).get(request, *args, **kwargs)


class SaveEventView(View):

    def post(self, request):
        color = request.POST.get('color')
        oldX = request.POST.get('oldX')
        oldY = request.POST.get('oldY')
        newX = request.POST.get('newX')
        newY = request.POST.get('newY')
        dashboard_id = request.POST.get('dashboard_id')
        save_event(color, oldX, oldY, newX, newY, dashboard_id)
        return HttpResponse(json.dumps({'success': 'true'}), mimetype='application/json')


class GetEventsView(View):

    def post(self, request):
        dashboard_id = request.POST.get('dashboard_id')
        events = get_events(dashboard_id)
        return HttpResponse(json.dumps({'events': events}), mimetype='application/json')
