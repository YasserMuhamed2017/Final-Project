from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('project/', views.project, name='project'),
    path('donate/<int:project_id>/', views.donate, name='donate'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]