"""
URL configuration for webapps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lanturnfly import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.map, name="home"),
    path('map/', views.map, name = "map"),
    # path('accounts/login/', views.login_action, name='login2'),
    # path('login', views.login_action, name="login"),
    # path('register', views.register_action, name='register'),
    path('add_report', views.add_report, name="add_report"),
    path('logout', auth_views.logout_then_login, name='logout'),
    # path('logout', views.logout_action, name="logout"), 
    # path('debug', views.all_report_debug, name="debug"), 
    path('myreport', views.my_report, name="myreport"), 
    path('photo/<int:id>', views.get_photo, name="photo"), 
    path('heatmap', views.heatmap, name="heatmap"),



    path('other_profile/<int:id>', views.other_profile_action, name='other_profile'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('follow/<int:id>', views.follow, name='follow'),

    path('global', views.global_action, name='global'),
    path('lanturnfly/get-global', views.get_global, name='get-global'),
    path('lanturnfly/add-comment', views.add_comment, name="add-comment"),

    path('oauth/', include('social_django.urls', namespace='social')),

]
