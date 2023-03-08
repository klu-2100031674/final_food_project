from django.urls import path
from foodauth import views
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.Handlelogin,name='login'),
    path('logout/',views.Handlelogouts,name='logout'),
    path('signupforadmin/',views.signupforadmin,name='loginforadmin'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),
]