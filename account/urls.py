from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # the login,logout,password_change,password_reset,password_change/done these url is django build in,if you don't write in here,no problem,these url works fine
    # post views
    # path('login/', views.user_login, name='login'),
    # Django built in authentication (no views model needed) which one is denoted by 'auth'
    # after successfully login the url is login and using build in registration/login.html template
    # login,logout,password_chang,password_change_done,password_reset,password_reset_done is django build in,there
    # no need to create view function,search template from templates/registration/url_name file
    path('login/', auth_views.LoginView.as_view(), name='login'), # Django build in class based authentication view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # use logout template
    path('', views.dashboard, name='dashboard'),
    # here using django built in authentication views for password change
    # passwordchangeview will handle the form to change the password
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    # passwordchangedoneview will display a success message after the user has successfully changed his password
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    # reset password url using django authentication
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # alternative way to authentication url
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]