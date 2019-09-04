from django.conf.urls import url
from .views import Event

urlpatterns = [
    url(r'^do', Event.as_view()),
]