from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('search',views.search,name = 'explore'),
    path('login',views.login_user,name = 'login'),
    path('register',views.registerUser,name = 'registeruser'),
    path('check_otp',views.check_otp,name = 'check_otp'),
    path('logout',views.logout_user,name = 'logout'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('show_userdata',views.show_userdata,name='show_userdata'),
    path('userdetails/<int:pk>',views.userdetails,name='userdetails'),
    path('parentdetails/<int:pk>',views.parentdetails,name='parentdetails'),
    path('preferencedetails/<int:pk>',views.preferencedetails,name='preferencedetails'),
    path('showimage/<int:pk>',views.showimage,name='showimage'),
    path('showprofile/<int:pk>',views.showprofile,name='showprofile'),
    path('choosemembership/<int:pk>',views.chooseMembership,name='choosemembership'),
    path('managemembership/<int:pk>',views.managemembership,name='managemembership'),
    path('interest',views.userInterest,name='interest'),
    path('deactivate',views.account_deactivate,name='deativateaccount'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = 'registered_user/password_reset.html'),name = 'reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = 'registered_user/password_reset_sent.html'), name= 'password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'registered_user/password_reset_form.html'), name = 'password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'registered_user/password_reset_done.html'),name = 'password_reset_complete'),
    path('gologin',views.gologin,name='gologin'),

]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)