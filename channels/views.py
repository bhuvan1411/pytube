from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Channel

class ChannelListView(ListView):
    model = Channel
    template_name = 'channels/list.html'

class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'channels/detail.html'

class ChannelCreateView(LoginRequiredMixin, CreateView):
    model = Channel
    fields = ['name', 'description']
    template_name = 'channels/form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ChannelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Channel
    fields = ['name', 'description']
    template_name = 'channels/form.html'

    def test_func(self):
        return self.request.user == self.get_object().owner

class ChannelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Channel
    template_name = 'channels/confirm_delete.html'
    success_url = reverse_lazy('channels:list')

    def test_func(self):
        return self.request.user == self.get_object().owner
