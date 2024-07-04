from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . models import Profile, Contribution,Month,Chat,Product,Theimages,ConfirmPayment
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def home(request):
    # Search functionality
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(Q(productname__icontains=q) | Q(productdescription__icontains=q))

    # Collect and save products to the backend
    if request.method == "POST":
        productimage = request.FILES.get('productimage')
        productname = request.POST['productname']
        productprice = request.POST['productprice']
        productdescription = request.POST['productdescription']

        new_product = Product(productimage=productimage, productname=productname, productprice=productprice, productdescription=productdescription)
        new_product.save()

        # After saving the new product, include it in the queryset
        products = Product.objects.all()
    
    profile = Profile.objects.all()
    chats = Chat.objects.all().order_by('-id')
    
   
    
    user_profile = None
    if request.user.is_authenticated:
        user_profile,created = Profile.objects.get_or_create(user=request.user)

    try:
        images = Theimages.objects.latest('id')
    except Theimages.DoesNotExist:
        images = None

    return render(request, 'home.html', {'profile': profile, 'user_profile': user_profile, 'chats': chats, 'products': products,'images':images})


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
    profile,created = Profile.objects.get_or_create(user=request.user)
    
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
    confirmed = ConfirmPayment.objects.filter(contribution=month.contribution).first()
    
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
        'confirmed':confirmed,
        
    }
    return render(request,'contribution.html',context)

@login_required(login_url='loging')
def months(request):
    if request.method == 'POST':
        monthname = request.POST['monthname']
        monthname=Month(monthname=monthname)
        monthname.save()
    months = Month.objects.all()
    month_length=months.count()
    context = {
        'months':months,
        'month_length':month_length,
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

def delete_chat(request,pk):
    chats = Chat.objects.get(pk=pk)
    chats.delete()
    return redirect('chat')

def delete(request,pk):
    contributions = Contribution.objects.get(pk=pk)
    if request.method == "POST":

        contributions.delete()
        return redirect('pictures')
    return render(request, 'delete.html')

def deleteproduct(request,pk):
    products = Product.objects.get(pk=pk)
    if request.method == "POST":

        products.delete()
        return redirect('home')
    return render(request, 'delete.html')

def confirmdelete(request):
    return render(request,'confirmdelete')

@login_required(login_url='loging')
def pictures(request):
    contributions = Contribution.objects.all()

    if request.method == "POST":
        contribution_id = request.POST['contribution_id']
        confirm = request.POST['confirm']
        try:
            contribution = Contribution.objects.get(id=contribution_id)
            ConfirmPayment.objects.update_or_create(contribution=contribution, defaults={'confirm': confirm})
        except Contribution.DoesNotExist:
            messages.error(request, "Contribution ID does not exist")
        
        return redirect('pictures')
    
    context = {
        'contributions': contributions
    }
    return render(request, 'pictures.html', context)



def myusers(request):
    users = User.objects.all()
    return render(request,'myusers.html',{"users":users})

def imagess(request):
    if request.method == "POST":
        pimage=request.FILES.get('pimage')
        bodyimage=request.FILES.get('bodyimage')
        logoimage=request.FILES.get('logoimage')
        newimage = Theimages(pimage=pimage,bodyimage=bodyimage,logoimage=logoimage)
        newimage.save()
    return render(request,'imagess.html')