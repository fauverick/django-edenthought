from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name = ''),
    path('register', views.register, name = "register"),
    path('dashboard', views.dashboard, name = "dashboard"),
    path('my_login', views.my_login, name = "my_login"),
    path("user_logout", views.user_logout, name = "user_logout"),
    path('create_thought', views.create_thought, name = "create_thought"),
    path('my_thoughts', views.my_thoughts, name = "my_thoughts"),
    path('update_thought/<str:pk>', views.update_thought, name = "update_thought"), # /<str:pk> to make the url dynamic
    path('delete_thought/<str:pk>', views.delete_thought, name = "delete_thought"), #to make the url dynamic
    path('profile_management', views.profile_management, name = "profile_management"),
    path('delete_account', views.delete_account, name = "delete_account"),

    #password management

    #allow to send email to reset password
    path('reset_password', auth_views.PasswordResetView.as_view(template_name = "journal/password_reset.html"), name = "reset_password"),

    #show success message that the email has been sent
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name = "journal/password_reset_sent.html"), name = 'password_reset_done'),

    #send a link to our email to reset password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "journal/password_reset_form.html"), name = "password_reset_confirm"),

    #show success message that password's been changed
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name = "journal/password_reset_complete.html"), name = 'password_reset_complete'),

]
