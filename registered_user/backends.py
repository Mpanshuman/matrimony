from django.contrib.auth.backends import ModelBackend
from registered_user.models import MyUser


## changes in authenticate so that user can login using both mobile number and email

class MyUserBackend(ModelBackend):

    def authenticate(self,request,**kwargs):
        
        phone = kwargs['email']
        password = kwargs['password']
        
        try:
            
            myuser = MyUser.objects.get(phone=phone)
            
            if myuser.check_password(password) is True:
                return myuser
        
        except MyUser.DoesNotExist:
            
            return None
