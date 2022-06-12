from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from pochven.models import SolarSystem, Constellation


class RootView(TemplateView):
    template_name = 'scouting.html'

    def get(self, request, **kwargs):

        if not request.user.is_authenticated:
            return redirect("username-login")

        return super().get(request, **kwargs)

    def post(self, request, **kwargs):

        if not request.user.is_authenticated:
            return redirect('/')

        if request.POST.get("action") == "reset":
            SolarSystem.objects.filter(
                claimed_by__isnull=False
            ).update(
                claimed_by=None
            )
            messages.success(request, "Successfully cleared scout assignments")

        if claim_system_id := request.POST.get("claim-system"):
            SolarSystem.objects.filter(
                id=claim_system_id
            ).update(
                claimed_by=request.user
            )

        if remove_claim_id := request.POST.get("remove-claim"):
            SolarSystem.objects.filter(
                id=remove_claim_id,
                claimed_by=request.user,
            ).update(
                claimed_by=None
            )

        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        constellations = Constellation.objects.all().prefetch_related(
            Prefetch('solarsystem_set', queryset=SolarSystem.objects.order_by('constellation', 'order'))
        )
        context['constellations'] = constellations
        return context


class UsernameLoginView(TemplateView):
    template_name = "username.html"

    def post(self, request, **kwargs):
        errors = {}

        if username := request.POST.get("username"):
            user, _ = User.objects.get_or_create(username=username)
            login(request, user)
            return redirect('/')

        else:
            errors["username"] = "Username is required"

        context = self.get_context_data(errors=errors, **kwargs)
        return self.render_to_response(context)


class Logout(View):

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("username-login")
