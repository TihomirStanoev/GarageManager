import django.contrib.auth.views as auth_views
from django.urls import path, reverse_lazy, include
from accounts import views


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above

app_name = 'accounts'

password_reset_urlpatterns = [
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
            email_template_name = 'accounts/password_reset_email.html',
            template_name = 'accounts/password_reset_form.html',
            subject_template_name = 'accounts/password_reset_subject.txt',
            success_url = reverse_lazy('accounts:password_reset_done'),),
        name='password_reset'),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name = 'accounts/password_reset_done.html'),
        name='password_reset_done',),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name = 'accounts/password_reset_confirm.html',
            success_url = reverse_lazy('accounts:password_reset_complete'),),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name = 'accounts/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]

urlpatterns = [
    path('', include(password_reset_urlpatterns)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.GarageLoginView.as_view(), name='login'),
    path('logout/', views.GarageLogoutView.as_view(), name='logout'),
]