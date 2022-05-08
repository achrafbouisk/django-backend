from django.urls import re_path, path
from . import views
from .views import RegisterView, LoginView, UserView, LogoutView, PostDetail

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path(r'^post$',views.postApi),
    path('post/<int:pk>/', PostDetail.as_view()),

    re_path(r'^comment$',views.commentApi),
    re_path(r'^reply$',views.replyApi),
    # re_path(r'^comment/([0-9]+)$',views.commentApi),

    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    
] 