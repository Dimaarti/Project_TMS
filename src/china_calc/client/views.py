from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from china_calc.client.forms import ClientForm
from china_calc.client.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = "client"

    def get_queryset(self):
        return (
            Client.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("item")
            .order_by("id")
        )


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "client/client_create.html"
    success_url = reverse_lazy("client:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
