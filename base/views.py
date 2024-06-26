from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . models import Profile, Contribution,Month,Chat,Product
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    profile = Profile.objects.all()
    products = Product.objects.all()
    chats = Chat.objects.all().order_by('-id')
    
    user_profile = None
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
    return render(request,'home.html',{'profile':profile,'user_profile':user_profile,'chats':chats,'products':products})
def perproduct(request,pk):
    products=Product.objects.get(pk=pk)
    return render(request,'perproduct.html',{'products':products})

def signup(request):
    
    #profile_user=Profile.objects.get(user=request.user)
    if request.method == "POST":
        username=request.POST['username'].lower()
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,password=password,email=email)
                user.save()
                #Here is where i redirect the user to create a profile 
                user = auth.authenticate(username=username,password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('create_profile')
        else:
            messages.info(request,'Passwords do not match')
            return redirect('signup')
    return render(request,'signup.html')

def loging(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username=request.POST['username'].lower()
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('loging')
    else:
        return render(request,'loging.html')

def logout(request):
    
    auth.logout(request)
    return redirect("home")

def profile(request):
    #To update my profile field
    profile = Profile.objects.get(user=request.user)
    
    if request.method=="POST":
        profile.profileimage=request.FILES.get('profileimage',profile.profileimage)
        profile.firstname=request.POST['firstname']
        profile.lastname=request.POST['lastname']
        profile.state=request.POST['state']
        profile.phonenumber=request.POST['phonenumber'] 
        profile.save()
        return redirect('home')
    #To display the profile field
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request,'profile.html',context)

def create_profile(request):
    if request.method=="POST":
        profile = Profile(
            user = request.user,
            profileimage=request.FILES.get('profileimage'),
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            state=request.POST['state'],
            phonenumber=request.POST['phonenumber'],
        )
        profile.save()
        return redirect('home')
    return render(request,'create-profile.html')

@login_required(login_url='loging')
def contribution(request,pk):
    month = Month.objects.get(pk=pk)
    #contributionimage = Contribution.objects.get(user=request.user)
    if request.method == "POST":
        contributionimage = request.FILES.get('contributionimage')
        contribution = Contribution(user=request.user,contributionimage=contributionimage)
        contribution.save()
        

        month.contribution = contribution
        month.save()
        return redirect('months')
        
    context = {
        
        'month':month,
        
    }
    return render(request,'contribution.html',context)

@login_required(login_url='loging')
def months(request):
    months = Month.objects.all()
    context = {
        'months':months,
    }
    return render(request,'months.html',context)

@login_required(login_url='loging')
def chat(request):
    chats = Chat.objects.all()
    
    if request.method=="POST":
        texts = request.POST['texts']
        chats = Chat(texts=texts,user=request.user).save()
    
        return redirect('chat')
    return render(request,'chat.html',{'chats':chats})

def delete(request,pk):
    chats = Chat.objects.get(pk=pk)
    chats.delete()
    return redirect('home')