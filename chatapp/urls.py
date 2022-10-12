from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home"),
    path('logout/', views.logout, name="logout"),
    path('chat/<str:username>', views.chat, name="chat")
]
