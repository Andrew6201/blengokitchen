from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('loging/',views.loging,name='loging'),
    path('logout/',views.logout,name='logout'),
    path('create_profile/',views.create_profile,name='create_profile'),
    path('profile/',views.profile,name='profile'),
    path('contribution/<str:pk>/',views.contribution,name='contribution'),
    path('months/',views.months,name='months'),
    path('chat/',views.chat,name='chat'),
    path('delete/<str:pk>/',views.delete,name='delete'),
    path('delete_chat/<str:pk>/',views.delete_chat,name='delete_chat'),
    path('perproduct/<str:pk>/',views.perproduct,name='perproduct'),
    path('pictures/',views.pictures,name='pictures'),
    path('confirmdelete/',views.confirmdelete,name='confirmdelete'),
    path('myusers/',views.myusers,name='myusers'),
    path('imagess/',views.imagess,name='imagess'),

    path('deleteproduct/<str:pk>/',views.deleteproduct,name='deleteproduct'),
    path('update-profile/<str:pk>/',views.update_profile,name='update-profile'),
    path("confirmed-users/",views.confirmed_users,name='confirmed-users'),
    path('notifications/',views.notifications,name='notifications'),
    path('order/',views.order,name='order'),
    path('all-orders/',views.all_orders,name='all-orders'),
    path('delete-order/<str:pk>/',views.deleteorder,name='delete-order'),
    path('about/',views.about,name='about'),
    path('deleteabout/<str:pk>/',views.deleteabout,name='deleteabout'),
    path('contact/',views.contact,name='contact'),
    
]