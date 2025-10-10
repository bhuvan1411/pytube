from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root redirects to channel list
    path('', lambda request: redirect('channels:list'), name='home'),
    path('channels/', include('channels.urls', namespace='channels')),
]
