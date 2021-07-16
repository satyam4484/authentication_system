from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginUser,name='login'),
    path('signup/',views.SignupUser,name='signup'),
    path('reserPassword/',views.resetPasswordUser,name='resetPassword'),
    path('reset/',views.resetpass,name='resetpass'),
    path('ChangePassword/',views.ChangePasswordUser,name='changePassword'),
    path('logout/',views.logoutUser,name='logout'),
    path('verify/<slug:token>',views.verifyuser,name='verify'),
    path('verifyr/<slug:token>',views.verifyr,name='verify'),

]
