from django.urls import path
from . import views
urlpatterns =[
    path('signup/', views.SignUpForm.as_view() , name='signup'),
    path('login/', views.LoginForm.as_view() , name='login'),
    path('carprofile/<int:id>',views.carprofile, name='carprofile'),
    path('profile/',views.buycar, name='profile'),
    path('update/', views.EditProfileView.as_view(), name='updateprofile'),
    path('buycar/<int:id>',views.buycar, name='buycar'),
    path('logout/',views.userlogout, name='logout'),

]