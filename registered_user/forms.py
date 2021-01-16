from django.forms import ModelForm
from registered_user.models import Parents_Details, User_Details, Image, Preference
from django import forms
class MakeForm(ModelForm):
    class Meta:
        model = Parents_Details
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User_Details
        exclude = ('user','profile_pic')
        fields = '__all__'
        
class ParentForm(ModelForm):
    class Meta:
        model = Parents_Details
        exclude = ('user',)
        fields = '__all__'

class ImageForm(ModelForm):
    class Meta:
        model= Image
        exclude = ('user',)
        fields= ["name", "imagefile"]

class PreferenceForm(ModelForm):
    class Meta:
        model = Preference
        exclude = ('user',)
        fields = '__all__'