from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('channels/', include(('channels.urls', 'channels'), namespace='channels')),
    path('videos/', include('videos.urls', namespace='videos')),

]
