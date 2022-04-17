from django.db import router
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('contact', views.ContactViewSet)

urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path("search/", views.search.as_view(), name="search"),
    path("find/", views.find.as_view(), name="find"),
    path("create/", views.CreateProfile.as_view(), name="create_profile"),
    path("register", views.Register.as_view(), name="register"),
    path("login", auth_views.LoginView.as_view(
        template_name="phonebook/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(
        template_name="phonebook/logout.html"), name="logout"),
    path("edit_profile/<int:pk>", views.EditProfile.as_view(), name="editprofile"),
    path("recent", views.Recent.as_view(), name="recent"),
    path("print/", views.PrintContact.as_view(), name="print"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls))
]
