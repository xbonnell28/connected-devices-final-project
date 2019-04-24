from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Lampi
from django.conf import settings
from lampi.forms import AddLampiForm
from .management.commands.analytics import KeenEventRecorder

keen_credentials = settings.KEEN_CREDENTIALS


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'lampi/index.html'

    def get_queryset(self):
        results = Lampi.objects.filter(user=self.request.user)
        return results

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['keen'] = {'project_id': keen_credentials['project_id'],
                           'write_key': keen_credentials['write_key']}
        return context


class DetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'lampi/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['keen'] = {'project_id': keen_credentials['project_id'],
                           'write_key': keen_credentials['write_key']}
        context['device'] = get_object_or_404(
            Lampi, pk=kwargs['device_id'], user=self.request.user)
        return context


class AddLampiView(LoginRequiredMixin, generic.FormView):
    template_name = 'lampi/addlampi.html'
    form_class = AddLampiForm
    success_url = '/lampi'

    def get_context_data(self, **kwargs):
        context = super(AddLampiView, self).get_context_data(**kwargs)
        context['keen'] = {'project_id': keen_credentials['project_id'],
                           'write_key': keen_credentials['write_key']}
        return context

    def form_valid(self, form):
        device = form.cleaned_data['device']
        device.associate_and_publish_associated_msg(self.request.user)
        keen = KeenEventRecorder(settings.KEEN_CREDENTIALS['project_id'],
                                 settings.KEEN_CREDENTIALS['write_key'])
        evt = {'device_id': device.device_id, 'user': device.user.username}
        keen.record_event('activations', evt)
        return super(AddLampiView, self).form_valid(form)


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'lampi/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['keen'] = {'project_id': keen_credentials['project_id'],
                           'read_key': keen_credentials['read_key']}
        return context
