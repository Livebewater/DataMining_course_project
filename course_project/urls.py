"""course_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from book_rate import views
from django.conf.urls import include, url
import debug_toolbar

urlpatterns = [

    path("", views.index),
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path("recent/", views.recent),
    path("popular/", views.popular),
    path("search/", views.search),
    path("books/<str:book_id>", views.book_detail),
    path("search/result/", views.search_return, name="search res"),
    path("accounts/", views.index),
    path("accounts/signup", views.signup),
    path("accounts/signup_process", views.signup_process, name="signup"),
    path("accounts/login", views.login),
    path("accounts/login_process", views.login_process, name="accounts"),
    path("accounts/<int:user_id>", views.login_success),
    path("accounts/<int:user_id>/my_rate", views.show_rate),
    path("accounts/<int:user_id>/my_rate/delete", views.delete_rate),
    path("accounts/<int:user_id>/my_rate/alter", views.alter_rate),
    path("accounts/<int:user_id>/search", views.search),
    path("accounts/<int:user_id>/search/result/", views.search_return, name="search res"),
    path("accounts/<int:user_id>/add_rate", views.add_rate, name="search res"),
]
