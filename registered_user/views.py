from django.shortcuts import render,redirect
from registered_user.models import MyUser, Image
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from non_registered_user.models import User_Test 
from registered_user.models import User_Details, Membership, Interest, Preference, Parents_Details
from django.contrib.auth.decorators import login_required
from random import randint
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import requests
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from registered_user.forms import UserForm, ImageForm, PreferenceForm, ParentForm
from django.core.paginator import Paginator,EmptyPage
from .models import *
from datetime import date
from dateutil.relativedelta import relativedelta
import urllib.parse
from itertools import chain
# Create your views here.

@login_required
def search(request):
    query = request.GET.get('search')
    
    minage = request.GET.get('minage')
    maxage = request.GET.get('maxage')
    salary = request.GET.get('salary')
    caste = request.GET.get('caste')
    religion = request.GET.get('religion')
    gender = request.GET.getlist('gender')
    state = request.GET.get('state')
    filter_btn = request.GET.get('filterbtn')
    filtered = False
   
    filterList = [minage,maxage,salary,caste,religion,state,gender]
    
    check_filter = [None]*(len(filterList)-1)
    check_filter.append([])
    
    if query is None:
        
        userdetails = User_Details.objects.none()
        
    
    elif query == '':

        userdetails = User_Details.objects.none()
 
    
    elif len(query) > 50:

        userdetails = User_Details.objects.none()
      
    
    
    else:
    
        userdetails = User_Details.objects.filter(Q(FirstName__icontains= query) |
        Q(LastName__icontains= query))
    
    if filterList != check_filter:
        userdetails,filtered = filtered_users(filterList,check_filter)
    
    
    userdetails=check_account_status(request,userdetails)
    
    imagedata = get_imagedata(userdetails)
        

    interestdata = get_interestdata(request,userdetails)

    parentdetails = get_parentdetails(userdetails)

    userdataperpage = manage_page(request,list(zip(userdetails,imagedata,interestdata,parentdetails)))

    membershipstatus = getmembershipstatus(request)

    useridrt = request.POST.get("interest")
    useridel = request.POST.get("remove")
    
    if useridrt != None and int(useridrt) != request.user.id:
        addInterest(request,useridrt)
    
    if useridel !=None:
        removeInterest(request,useridel)
    param = {}
    if len(gender) == 0:
        param = {'userdetails':userdataperpage,'search':query,'membership':membershipstatus,'filtered_user':filtered,'religion':religion,'miage':minage,'maage':maxage,'salary':salary,'caste':caste,'state':state,'generlen':len(gender)}    
    elif len(gender) == 1 and gender[0] != '':
        param = {'userdetails':userdataperpage,'search':query,'membership':membershipstatus,'filtered_user':filtered,'religion':religion,'miage':minage,'maage':maxage,'salary':salary,'caste':caste,'state':state,'gender':gender[0],'generlen':len(gender)}
    elif len(gender) == 2:
        param = {'userdetails':userdataperpage,'search':query,'membership':membershipstatus,'filtered_user':filtered,'religion':religion,'miage':minage,'maage':maxage,'salary':salary,'caste':caste,'state':state,'gender1':gender[0],'gender2':gender[1],'generlen':len(gender)}
    elif len(gender) == 3:
        param = {'userdetails':userdataperpage,'search':query,'membership':membershipstatus,'filtered_user':filtered,'religion':religion,'miage':minage,'maage':maxage,'salary':salary,'caste':caste,'state':state,'gender1':gender[0],'gender2':gender[1],'gender3':gender[2],'generlen':len(gender)}
    
   
    return render(request,'registered_user/explore.html',param)

def login_user(request):
    
    try:
    
        if request.method == 'POST':
            username = request.POST['loginusername']
            password = request.POST['loginpassword']
            user_status = MyUser.objects.get(Q(email = username)| Q(phone = username))
    
            if not user_status.is_active:
                user_status.is_active = True
                user_status.save()

            user = authenticate(email = username , password = password)
        
            if user is not None:
                login(request,user)
                otp_gen(username)
                return redirect('index')
              
            else:
                return redirect('login')
    except:
        messages.info(request,'please use mobile no. or Email..')
        return redirect('login')


    else:
        return render(request,'registered_user/login.html')


def registerUser(request):
    
    if request.method == 'POST':

        # Getting Values from html form by name
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['emailaddress']

        # creating user in MyUser model(Custom model)
        validate = clean_phone(phone,username,email)
        if validate == True:
            myuser = MyUser.objects.create_user( username=username,email = email, password = password, phone=phone)


            check_otp(request)
            myuser.save()
       
            membership = Membership(user_id = myuser.id)
            membership.save()
        
            return redirect('index')
        else:
            messages.info(request,validate)
            return redirect('registeruser')

        ## Like above add Data in Personal,Parents and preference model
        # preference model not created yet...


        # {'Status': 'Success', 'Details': 'ddd8b058-da70-48ab-bdcf-e2a5fe50a359'}
        # otp = otp_gen(phone)
        # response = send_otp(request,phone=phone,otp=otp)
        # print(response)
        
        '''sent_mail will work for less secure app(gmail > account setting > less secure app > enabled)'''
        
        # #sent_email(username=username,email=email)
        # check_otp(request)
        # myuser.save()
       
        # membership = Membership(user_id = myuser.id)
        # membership.save()
        
        # return redirect('index')
    
    else:
        return render(request,'registered_user/registeration_user.html')


def check_otp(request):
    return render(request,'registered_user/otpcheck.html')


#for validation
def clean_phone(phone,username,email):
    for instance in MyUser.objects.all():    
        if instance.phone == phone:
            message = 'phone already exist'
            return message
        elif instance.username == username:
            message = 'username already exist'
            return message
        elif instance.email == email:
            message = 'email already exist'
            return message
    return True

def logout_user(request):
    
    logout(request)
    return redirect('index')


def userprofile(request):
    
    try:
        image_details= Image.objects.get(user_id= request.user.id)

    except Image.DoesNotExist:
        image_details = None
    
    try:
        membershipinfo = Membership.objects.get(user_id= request.user.id)
    except Membership.DoesNotExist:
        image_details = None

    username = request.user.username
    useremail = request.user.email
    userphone = request.user.phone
    userdatafromdb = get_userdata(request)
    userdata = {'UserName': username,'UserEmail': useremail, 'UserData':userdatafromdb,'UserPhone':userphone,'image_details':image_details, 'membership':membershipinfo}
    
    return render(request,'registered_user/userprofile.html',userdata)




def userdetails(request,pk):
    try:
        userdata = User_Details.objects.get(user_id = pk)
    except User_Details.DoesNotExist:
        userdata = None
        
    if userdata is not None:
        form = UserForm(instance = userdata)
    else:
        form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, instance=userdata)
        if form.is_valid():
            userdetailsform = form.save(commit=False)
            userdetailsform.user = request.user
            userdetailsform.save()

            
            return redirect('userprofile')

    return render(request,'registered_user/personaldetailsform.html',{'form':form})

def parentdetails(request,pk):
    try:
        userdata = Parents_Details.objects.get(user_id = pk)
    except Parents_Details.DoesNotExist:
        userdata = None
        
    if userdata is not None:
        form = ParentForm(instance = userdata)
    else:
        form = ParentForm()
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=userdata)
        if form.is_valid():
            userdetailsform = form.save(commit=False)
            userdetailsform.user = request.user
            userdetailsform.save()

            
            return redirect('userprofile')

    return render(request,'registered_user/parentsdetailsform.html',{'form':form})


def showprofile(request,pk):
    parentdata = None
    try:
        userdata = User_Details.objects.get(id = pk)
        
    except User_Details.DoesNotExist:
        userdata = None
        
    if userdata is not None:
        try:
            parentdata = Parents_Details.objects.get(user_id = userdata.user_id)
            
        except Parents_Details.DoesNotExist:
            parentdata = None
    print('parentdata:',parentdata)
     
    try:
        imagedata = Image.objects.get(user_id = userdata.user_id)
    except Image.DoesNotExist:
        imagedata = None
    
    membershipstatus = getmembershipstatus(request)


    # print('userdata:',imagedata.imagefile)
    userdata = {'userdata': userdata,'image': imagedata,'default':'images/default_pic.png','membership':membershipstatus,'parentdata': parentdata}
    return render(request,'registered_user/showprofile.html',userdata)

# def showuserinfo(request,pk):
#     try:
#         userdata = User_Details.objects.get(id = pk)
        
#     except User_Details.DoesNotExist:
#         userdata = None

#     # print('userdata:',imagedata.imagefile)
#     userdata = {'userdata': userdata,'membership':checkMembership(request)}
#     return render(request,'registered_user/showuserinfo.html',userdata)

# def showparentinfo(request,pk):
#     parentdata = None
#     try:
#         userdata = User_Details.objects.get(id = pk)
        
#     except User_Details.DoesNotExist:
#         userdata = None
    
#     if userdata is not None:
#         try:
#             parentdata = Parents_Details.objects.get(user_id = userdata.user_id)
            
#         except Parents_Details.DoesNotExist:
#             parentdata = None
#     print('parentdata:',parentdata)
#     parentdata = {'parentdata': parentdata}
#     return render(request,'registered_user/showuserparentsinfo.html',parentdata)
    
def chooseMembership(request,pk):
    if request.method == 'POST':
        sub_months = request.POST['btn']
        # print('btn:',months)
        if sub_months is not None:
            
            try:
                membershipdata = Membership.objects.get(user_id = pk)
            except Membership.DoesNotExist:
                membershipdata = None
            
            if membershipdata is not None and membershipdata.membership_start_data is None:
                membershipdata.membership = 'Premium'
                membershipdata.membership_start_data = date.today()
                membershipdata.membership_end_data = membershipdata.membership_start_data + relativedelta(months=+int(sub_months))
                membershipdata.save()
                
            else:
                membershipdata.membership = 'Premium'
                membershipdata.membership_end_data = membershipdata.membership_end_data + relativedelta(months=+int(sub_months))
                membershipdata.save()
               
    return render(request,'registered_user/choosemembership.html')


def managemembership(request,pk):
    try:
        membershipdata = Membership.objects.get(user_id = pk)
    except Membership.DoesNotExist:
        membershipdata = None
    
    if request.method == 'POST':
    
        membershipchoise = request.POST.get('manage-btn')
       
        if membershipchoise == 'cancel':

            membershipdata.membership = 'Free'
            membershipdata.membership_start_data = None
            membershipdata.membership_end_data = None
            membershipdata.save()
            return redirect('userprofile')
          
    
    membershipdata_context = {'membership':membershipdata}



    return render(request,'registered_user/managemembership.html',membershipdata_context)


def userInterest(request):
    userid = request.GET.get("interest")
    interesteduserslist = showInterestusers(request)
    membershipstatus = getmembershipstatus(request)
    useridrt = request.POST.get("remove")
    
    try:
        if useridrt is not None:
            removeInterest(request,useridrt)
            return redirect('interest')
    except Interest.DoesNotExist:
        pass
    interesteduserslist = {'interestedUsers': interesteduserslist,'membership':membershipstatus}
    return render(request,'registered_user/interest.html', interesteduserslist)


def preferencedetails(request,pk):
    try:
        preference = Preference.objects.get(user_id = pk)
    except Preference.DoesNotExist:
        preference = None
        
    if preference is not None:
        form = PreferenceForm(instance = preference)
    else:
        form = PreferenceForm()
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            preferenceform = form.save(commit=False)
            preferenceform.user = request.user
            preferenceform.save()
            return redirect('userprofile')

    return render(request,'registered_user/personaldetailsform.html',{'form':form})


def preferedusers(request):
    try:
        preference = Preference.objects.get(user_id = request.user.id)
    except Preference.DoesNotExist:
        preference = None
    
    if preference is not None:
        preferedsuser = User_Details.objects.none()
        preferedsuser = findage(userdata= preferedsuser,minage= int(preference.minAge))
        preferedsuser = findage(userdata= preferedsuser,maxage= int(preference.maxAge))
        preferedsuser = getsalary(userdata= preferedsuser, salary= int(preference.minSalary))
        preferedsuser = preferedsuser.filter(gender = preference.gender)
        
        # Sorting users on basis of salary in descending order

        preferedsuserdefault = preferedsuser.order_by("-salary")
        
    
        
        remainingfieldsvalues = [preference.caste, preference.religion,preference.state]
        remainingfields = ["caste","religion","state"]
        remainingfieldsdict = {}
        non_noneValues = [int(selectedfiledindex) for selectedfiledindex,selectedfiled  in enumerate(remainingfieldsvalues) if selectedfiled != None]
        filedslist_values = [remainingfields[fileds] for fileds in non_noneValues] 
        
        for i in non_noneValues:
            remainingfieldsdict[remainingfields[i]] = remainingfieldsvalues[i]

        preferedsuser = preferedsuser.filter(**remainingfieldsdict).order_by("-salary")
        imagedatadefault = get_imagedata(preferedsuserdefault)
        imagedata = get_imagedata(preferedsuser)
        imagedata = unique(list(chain(imagedata, imagedatadefault)))
        preferedsuser = unique(list(chain(preferedsuser, preferedsuserdefault)))
        
        
        return [preferedsuser,imagedata]
    else:
        return None
# OTP GENERATOR

def otp_gen(phone):
    if phone:
        otp = randint(999,9999)
        # print('OTP GENERATED: ',otp)
        return otp
    else:
        return False


# {"Status":"Success","Details":"9a34f389-e538-47a6-bf3a-80d097b29504"}

# Send OTP to the Registered Number if Valid
def send_otp(request,phone,otp):
    
    URL = f"https://2factor.in/API/V1/683f7e4e-191c-11eb-b380-0200cd936042/SMS/{phone}/{otp}/HASTA"
    
    response = requests.request('GET',URL)
    data = response.json()
    
    return data

'''sent_mail will work for less secure app(gmail > account setting > less secure app > enabled) 
   uncomment the sent_mail method to test
   settings.py > EMAIL_HOST_USER = 'Your Email Address'
                 EMAIL_HOST_PASSWORD = 'Your Email Address Password'
    
'''
def sent_email(username,email):
    
    template = render_to_string('registered_user/email_conformation.html',{'name':username})
    
    email = EmailMessage(
    'Thank you for choosing this site',
    template,
    settings.EMAIL_HOST_USER,
    [email],)
    email.fail_silently = False
    email.send()



def get_userdata(request):
    try:
        userdata = User_Details.objects.get(user_id=request.user.id)
    except User_Details.DoesNotExist:
        userdata = {'age':'-','dateofbirth':'-','religion':'-','gender':'-'}
    
    
    return userdata
def show_userdata(request):
    try:
        #userdata = User_Details.objects.get(user_id=request.user.id)
        userdata = User_Details.objects.filter(user_id = request.user.id).values()
        ctx = {'userdata':userdata}
    except User_Details.DoesNotExist:
        userdata = {'age':'-','dateofbirth':'-','religion':'-','gender':'-','profile_pic':'/images/defaultpic.png'}
        ctx = {'userdata':userdata}
    #print('User Data:', userdata)
    return render(request,'registered_user/user_details.html',ctx)


def manage_page(request,searchresult):
    
    p = Paginator(searchresult,1)
    pagenum = request.GET.get('page',1)
    
    try:
        page = p.page(pagenum)
    except EmptyPage:
        page = p.page(1)
    
    return page



#for image
def showimage(request,pk):
    
    try:
        imagefile= Image.objects.get(user_id= pk)
        
    except Image.DoesNotExist:
        imagefile = None
        


    if imagefile is not None:
        form = ImageForm(instance = imagefile)
    else:
        form = ImageForm()
    if request.method == 'POST':
        form= ImageForm(request.POST,request.FILES,instance = imagefile)
        if form.is_valid():
            imageviewform = form.save(commit = False)
            imageviewform.user = request.user
            imageviewform.save()
            
            return redirect('userprofile')

    
    context= {'imagefile': imagefile,
              'form': form
              }
    
      
    return render(request, 'registered_user/images_try.html', context)


#get image
def get_imagedata(userdetails):

    userdetails_value =  userdetails.values('user_id')
   
    res_lis = []
    user_list = [uid['user_id'] for uid in userdetails_value ]
    
    imgdetails = Image.objects.filter(user_id__in = user_list)
   
    imgdetails_values = imgdetails.values()
    
    imgdetails_values_id = imgdetails.values('user_id')
    
    img_list = [uid['user_id'] for uid in imgdetails_values_id ]
   
    for data in user_list:

        if data in img_list:
            res_lis.append('media/'+str(Image.objects.get(user_id = data).imagefile))
        else:
            res_lis.append("media/images/default_pic.png")

    return res_lis

def get_parentdetails(userdetails):
    userdetails_value =  userdetails.values('user_id')
    res_lis = []
    user_list = [uid['user_id'] for uid in userdetails_value ]
    try:
        parentsdetails = Parents_Details.objects.filter(user_id__in = user_list)
    except Parents_Details.DoesNotExist:
        parentsdetails = None
    parentsdetails_values = parentsdetails.values()
    
    parentsdetails_values_id = parentsdetails.values('user_id')
    parent_list = [uid['user_id'] for uid in parentsdetails_values_id]
    for data in user_list:
        if data not in parent_list:
            res_lis.append(None)
        else:
            res_lis.append(Parents_Details.objects.get(user_id = int(data)))
    print('parentdetails:',parentsdetails)
    print('parentsdetails_values_id:',parentsdetails_values_id)
    print('parentsdetails_list:', res_lis)
    return res_lis
def checkMembership(request):
    if not request.user.is_anonymous:
        today = date.today()
        membershipdata = Membership.objects.get(user_id = request.user.id)
        if membershipdata.membership != 'Free':

            if today > membershipdata.membership_end_data:
                membershipdata.membership = 'Free'
                membershipdata.membership_start_data = None
                membershipdata.membership_end_data = None
                membershipdata.save()
         
      


def getmembershipstatus(request):
    if not request.user.is_anonymous:
        membershipdata = Membership.objects.get(user_id = request.user.id)
       
        return membershipdata


def addInterest(request,interesteduserid):
    if interesteduserid is not None:
        interest_users_list = Interest.objects.filter(interesteduser__in = interesteduserid)
        interest_list = [int(uid['interesteduser']) for uid in interest_users_list.values('interesteduser')]
        print('add list_:',interest_list)
        print('add userid:',interesteduserid)
        if(interesteduserid not in interest_list):
            print('add userid:',interesteduserid)
            try:
                interest = Interest(user_id = request.user.id, interesteduser = interesteduserid)
                interest.save()
                # sent_interest_mail(request,interesteduserid)
                print(interesteduserid,' added')
                
            except Interest.DoesNotExist:
                interest = Interest(user_id = request.user.id, interesteduser = interesteduserid)
                interest.save()
            


def getInterest(request):
    interest = Interest.objects.filter(user_id = request.user.id)
    return interest


def showInterestusers(request):
    interestedusers=getInterest(request)
    interesteduserid = [uid['interesteduser'] for uid in interestedusers.values('interesteduser') ]

    userdetails = User_Details.objects.filter(user_id__in = interesteduserid)
   
    image_details = get_imagedata(userdetails)

    userdataperpage = manage_page(request,list(zip(userdetails,image_details)))

    return userdataperpage

def removeInterest(request,interesteduserid):
    interest = Interest.objects.get(user_id = request.user.id, interesteduser = interesteduserid)
    
    interest.delete()
    


def get_interestdata(request,userdetails):
    userdetails_value =  userdetails.values('user_id')
   
    res_lis = []
    
    user_list = [uid['user_id'] for uid in userdetails_value ]
 
    
    interestdetails = Interest.objects.filter(Q(interesteduser__in = user_list) &
        Q(user_id = request.user.id))
    
    interestdetails_values_id = interestdetails.values('interesteduser')
    
    interest_list = [int(uid['interesteduser']) for uid in interestdetails_values_id ]
    
   
    for data in user_list:

        
        if data in interest_list:
            res_lis.append(data)
           
        else:
            
            res_lis.append(0)
       
    return res_lis


def sent_interest_mail(request,interested_userid):
    print('id:',interested_userid)
    user_data = User_Details.objects.get(user_id = interested_userid)
    current_user = User_Details.objects.get(user_id = request.user.id)
    print('username:', user_data.FirstName)
    print('email:', user_data.email)
    print('email:', User_Details.objects.get(user_id = request.user.id))
    template = render_to_string('registered_user/interest_email.html',{'name':user_data.FirstName,'currentuser':current_user.FirstName})
    
    email = EmailMessage(
    'Someone is simping on you..',
    template,
    settings.EMAIL_HOST_USER,
    [user_data.email],)
    email.fail_silently = False
    email.send()


def account_deactivate(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect('index')



def check_account_status(request,userdetails):
    
    #exclude the logged in user in the search result
    resultusers = userdetails.exclude(user_id = request.user.id)

    resultusersid = [int(uid['user_id']) for uid in resultusers.values('user_id')]
    userstatus = MyUser.objects.filter(id__in = resultusersid)
    activeusers_list = [user.id for user in userstatus if(user.is_active)]
    activeusers = userdetails.filter(user_id__in = activeusers_list)
    print('active Users:',activeusers)
    return activeusers


def filtered_users(filter_user,check_filter):
   
    onclick_list = ['']*(len(check_filter)-1)
    onclick_list .append([])
    
    oyeah = User_Details.objects.none()
    
    minage = filter_user[0]
    maxage = filter_user[1]
    salary = filter_user[2]
    caste = filter_user[3]
    religion = filter_user[4]
    state = filter_user[5]
    gender = filter_user[6]
    
    non_noneValues = []
    
    query_dict = {}
    
    filedslist = ['minage','maxage','salary','caste','religion','state','gender']
    
    non_noneValues = [int(selectedfiledindex) for selectedfiledindex,selectedfiled  in enumerate(filter_user) if selectedfiled != '']
    filedslist_values = [filedslist[fileds] for fileds in non_noneValues]
    
    
    for query_index in non_noneValues:
        filterd_user = True
        if query_index not in [0,1,2,6]:
            query_dict[filedslist[query_index]] = filter_user[query_index]
            
    
        if query_index == 0:
            
            if minage is not None:
                oyeah = findage(minage=int(minage),userdata= oyeah)
            
        
        if query_index == 1:
            
            if maxage is not None:
                oyeah = findage(maxage=int(maxage),userdata= oyeah)
            
        
        if  query_index == 2:
            if salary is not None:
                oyeah = getsalary(oyeah, salary = int(salary))

        if query_index == 6:
            
            oyeah = getgender(oyeah,genderlist= gender)

    
    if filter_user != check_filter or filter_user != onclick_list:
        
        if bool(query_dict) == True and oyeah.exists():
            oyeah = oyeah.filter(**query_dict)
        elif bool(query_dict) == True and not oyeah.exists():
            oyeah = User_Details.objects.filter(**query_dict)
       
    else:
        filterd_user = False
        oyeah = User_Details.objects.none()
    
    print('oyeah:',oyeah)
    return oyeah,filterd_user


def findage(userdata,minage = None, maxage = None ):
    
    if userdata.exists() and minage is not None:
        
        userdata = userdata.filter(age__gt = minage)
    
    elif  minage is not None:
        
        userdata = User_Details.objects.filter(age__gt = minage)
    
    elif userdata.exists() and maxage is not None:
        
        userdata = userdata.filter(age__lt = maxage)
    
    elif maxage is not None:
        
        userdata = User_Details.objects.filter(age__lt = maxage)
    
    return userdata



def getsalary(userdata,salary = None):
    
    if salary is not None and userdata.exists():
        userdata = userdata.filter(salary__gt = salary)
    elif  salary is not None and not userdata.exists():
        userdata = User_Details.objects.filter(salary__gt = salary)
    
    return userdata


def getgender( userdata,genderlist = []):
    
    if len(genderlist) > 0 and userdata.exists():
        userdata = userdata.filter(gender__in = genderlist)
    
    elif  len(genderlist) > 0 and not userdata.exists():
        userdata = User_Details.objects.filter(gender__in = genderlist)
    return userdata

def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x)
    return unique_list

#google login

def gologin(request):
    return render(request,'registered_user/sociallogin.html')