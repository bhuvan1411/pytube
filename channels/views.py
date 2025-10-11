# channels/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Channel

# -------------------------
# Create Channel
# -------------------------
@method_decorator(login_required, name='dispatch')
class ChannelCreateView(CreateView):
    model = Channel
    fields = ['name', 'description']
    template_name = 'channels/form.html'
    success_url = reverse_lazy('channels:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# -------------------------
# List Channels
# -------------------------
class ChannelListView(ListView):
    model = Channel
    template_name = 'channels/list.html'
    context_object_name = 'channels'  # optional, for clarity in template

# -------------------------
# Channel Detail
# -------------------------
class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'channels/detail.html'
    context_object_name = 'channel'

# -------------------------
# Update Channel
# -------------------------
class ChannelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Channel
    fields = ['name', 'description']
    template_name = 'channels/form.html'
    success_url = reverse_lazy('channels:list')

    def test_func(self):
        # Only allow the owner of the channel to update it
        return self.request.user == self.get_object().owner

# -------------------------
# Delete Channel
# -------------------------
class ChannelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Channel
    template_name = 'channels/confirm_delete.html'
    success_url = reverse_lazy('channels:list')

    def test_func(self):
        # Only allow the owner of the channel to delete it
        return self.request.user == self.get_object().owner
