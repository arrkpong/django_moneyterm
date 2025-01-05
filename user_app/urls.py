from django.urls import path
from django.contrib.auth import views as auth_views
from user_app.views import RegisterView, LoginView, LogoutView, ProfileView, EditProfileView, ChangePasswordView
from django.contrib.auth.forms import PasswordResetForm

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html',form_class=PasswordResetForm), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
