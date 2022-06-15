from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView
from django_registration import signals
from django_registration.views import RegistrationView as _RegistrationView

from pochven.models import Constellation, SolarSystem


class RootView(TemplateView):
    template_name = "scouting.html"

    def get(self, request, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        return super().get(request, **kwargs)

    def post(self, request, **kwargs):

        if not request.user.is_authenticated:
            return redirect("/")

        action = request.POST.get("action")

        if action == "clear-self":
            self.handle_clear_self(request)

        if action == "reset":
            self.handle_scout_reset(request)

        if claim_system_id := request.POST.get("claim-system"):
            SolarSystem.objects.filter(id=claim_system_id).update(
                claimed_by=request.user
            )

        if remove_claim_id := request.POST.get("remove-claim"):
            SolarSystem.objects.filter(
                id=remove_claim_id,
                claimed_by=request.user,
            ).update(claimed_by=None)

        return redirect("/")

    def handle_clear_self(self, request):

        SolarSystem.objects.filter(claimed_by=request.user).update(claimed_by=None)

    @method_decorator(
        permission_required(
            perm="pochven.reset_scout",
            raise_exception=True,
        )
    )
    def handle_scout_reset(self, request):

        SolarSystem.objects.filter(claimed_by__isnull=False).update(claimed_by=None)
        messages.success(request, "Successfully cleared scout assignments")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        constellations = Constellation.objects.all().prefetch_related(
            Prefetch(
                "solarsystem_set",
                queryset=SolarSystem.objects.order_by("constellation", "order"),
            )
        )
        context["constellations"] = constellations
        return context


class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("root")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class Logout(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("login")


class RegistrationView(_RegistrationView):
    template_name = "register.html"
    success_url = reverse_lazy("root")

    def register(self, form):
        new_user = form.save()
        new_user = authenticate(
            **{
                User.USERNAME_FIELD: new_user.get_username(),
                "password": form.cleaned_data["password1"],
            }
        )
        login(self.request, new_user)
        signals.user_registered.send(
            sender=self.__class__, user=new_user, request=self.request
        )
        messages.success(self.request, "You successfully registered.")
        return new_user

    def get_success_url(self, user=None):
        return reverse_lazy("root")

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url(self.register(form)))
