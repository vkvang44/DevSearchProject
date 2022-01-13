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

    # path('create_exp/', views.createExperience, name='create_exp'),
    # path('update_exp/<str:pk>', views.updateExperience, name='update_exp'),
    # path('delete_exp/<str:pk>', views.deleteExp, name='delete_exp'),

    path('inbox/', views.inbox, name='inbox'),
    path('message_page/<str:pk>', views.messagePage, name='message_page'),
    path('send_message/<str:pk>', views.sendMessage, name='send_message'),
]