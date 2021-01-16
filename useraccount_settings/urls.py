from django.urls import path
from . import views
urlpatterns = [
    path('',views.accountsetting,name = 'accountsetting'),
    path('changepassword',views.changepasswordtemplate,name = 'changepassword'),
    path('deactivateaccount',views.deactivateAccount,name = 'deactivateaccount'),
]