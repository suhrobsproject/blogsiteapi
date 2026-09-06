from django.urls import path
from .views import SignUpView, LoginView, ProfileView, ProfileUpdateView, PassChangeView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', ProfileView.as_view()),
    path('update/', ProfileUpdateView.as_view()),
    path('update/', ProfileUpdateView.as_view()),
    path('pass-change/', PassChangeView.as_view()),
    path('logout/', LogoutView.as_view()),
]
