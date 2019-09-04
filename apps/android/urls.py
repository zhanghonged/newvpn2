from django.conf.urls import url
from .views import ClientUser, Test, test2

urlpatterns = [
    url(r'^init', ClientUser.as_view(), name="go"),
    url(r'^test',Test.as_view()),
    url(r'^aaa', test2)
]