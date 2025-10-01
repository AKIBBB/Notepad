from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("notes/", views.notes, name="notes"),
    path("notes/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("notes/<int:note_id>/delete/", views.delete_note, name="delete_note"),
    path("notes/<int:note_id>/download/", views.download_note, name="download_note"),


]
