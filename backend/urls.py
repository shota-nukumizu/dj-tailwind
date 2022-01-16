from django.contrib import admin
from django.urls import path

from todo.views import todos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', todos, name='todo'),
]
