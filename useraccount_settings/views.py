from django.shortcuts import render,redirect
from registered_user.models import MyUser
from registered_user.views import logout_user,chooseMembership,account_deactivate,getmembershipstatus,managemembership
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def accountsetting(request):
    if request.method == 'POST':
        changepassword_value = request.POST.get('changepassbtn')
        deactivate_value = request.POST.get('deactivatebtn')
        cancel_plan = request.POST.get('manage-btn')
        if(changepassword_value != None):
            changepassword(request)
            return redirect('index')
        
        elif (deactivate_value != None):
            deactivate_account_check(request)
            return redirect('index')
        
        elif(cancel_plan != None):
            print('hey')
            managemembership(request,request.user.id)
            
        else:   
            print('else') 
            chooseMembership(request,request.user.id)
    membershipdata = str(getmembershipstatus(request)).split(':')
    print('membership:',membershipdata[1].strip())
    param = {'membership':membershipdata[1].strip()}
    return render(request,'useraccount_settings/settings.html',param)


def changepasswordtemplate(request):
    if(changepassword(request)):
        return redirect('index')
    
    return render(request,"useraccount_settings/changepassword.html")

def deactivateAccount(request):
    return render(request,"useraccount_settings/deactivateaccount.html")

def changepassword(request):
    userdata = MyUser.objects.get(id = request.user.id)
    if request.method == "POST":
        oldpass = request.POST['oldpassword']
        newpass = request.POST['newpassword']
        confpass = request.POST['cnfpassword']
        if oldpass == confpass and userdata.check_password(oldpass):
            userdata.set_password(newpass)
            userdata.save()
            logout_user(request)
            
def deactivate_account_check(request):
    userdata = MyUser.objects.get(id = request.user.id)
    if request.method == "POST":
        confpass = request.POST['cnfpassword']
        if userdata.check_password(confpass):
            account_deactivate(request)
            logout_user(request)