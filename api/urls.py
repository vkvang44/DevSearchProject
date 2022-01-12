from django.urls import path
from . import views

# import views from simplejwt to implement json tokens for authentication
from rest_framework_simplejwt.views import (
    # generate json web token
    TokenObtainPairView,

    # generate json refresh token
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),

    path('remove_tag/', views.removeTag),
]