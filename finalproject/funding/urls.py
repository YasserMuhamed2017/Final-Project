from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('home/', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('project/', views.project, name='project'),
    path('donate/<int:project_id>/', views.donate, name='donate'),
    path('report_comment/<int:comment_id>/', views.report_comment, name='report_comment'),
    path('report_project/<int:project_id>/', views.report_project, name='report_project'),
    path('rate_project/<int:project_id>/', views.rate_project, name='rate_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('cancel_project/<int:project_id>/', views.cancel_project, name='cancel_project'),
    path('search/', views.search_projects, name='search_projects'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
]