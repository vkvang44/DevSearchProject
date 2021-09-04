from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('account/', views.userAccount, name='account'),
    path('edit_account/', views.editAccount, name='edit_account'),

    path('create_skill/', views.createSkill, name='create_skill'),
    path('update_skill/<str:pk>', views.updateSkill, name='update_skill'),
    path('delete_skill/<str:pk>', views.deleteSkill, name='delete_skill'),
]