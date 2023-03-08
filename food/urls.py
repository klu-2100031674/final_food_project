from django.urls import path
from food import views
urlpatterns = [
    path('',views.index,name='index'),
    path('smileycards/',views.smileycards, name = 'smilecards'),
    path('checkout/', views.checkout, name="Checkout"),
    path('contactus',views.contactus,name='contactus'),
    path('tracker', views.tracker, name="TrackingStatus"),
    path('handlerequest/', views.handlerequest, name="HandleRequest"),
    path('checkout/', views.checkout, name="Checkout"),
    path('profile/',views.profile,name ='profile'),
    path('todayspecial/',views.todayspecial,name ='todayspecial'),
    path('delivery/',views.delivery,name ='delivery'),
        path('delivery/breakfast/',views.breakfast,name ='breakfast'),
        path('delivery/lunch/',views.lunch,name ='lunch'),
        path('delivery/dinner/',views.dinner,name="dinner"),
        path('delivery/snacks/',views.snacks,name="snacks"),
        path('delivery/cafe/',views.cafe,name="cafe"),
    path('celibrate/',views.celeberate,name="celibrate"),
    path('ourspecials/',views.ourspecials,name="ourspecials"),
    path('about/',views.about,name="about"),
    

]