from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . models import Profile, Contribution,Month,Chat,Product,Theimages,ConfirmPayment,OrderMade,ContactMessage,AboutImages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from collections import defaultdict
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
    if request.method == "POST":
        username = request.POST['username'].lower()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if len(password) < 6:
            messages.info(request, 'Password should not be less than six characters')
            return redirect('signup')

        if not any(char in '@#$%*^?/\'"[]{}' for char in password):
            messages.info(request, 'Password must include at least one special character (e.g. @#$%*^?/\'"[])')
            return redirect('signup')

        if not any(char.isdigit() for char in password):
            messages.info(request, 'Password must include at least one number (e.g. 1234)')
            return redirect('signup')

        if not any(char.isalpha() for char in password):
            messages.info(request, 'Password must include at least one alphabet (e.g. abcd)')
            return redirect('signup')

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                return redirect('loging')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    return render(request, 'signup.html')

def loging(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is None:
            # Authentication failed, so check why it failed
            if not auth.models.User.objects.filter(username=username).exists():
                messages.info(request, "Incorrect username!")

            
            else:
                messages.info(request, "Incorrect password!")
            return redirect('loging')
        
        else:
            # Authentication was successful
            auth.login(request, user)
            return redirect('home')
            
    return render(request, 'loging.html')
'''
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
'''


def logout(request):
    
    auth.logout(request)
    return redirect("home")

def profile(request):

    #To display the profile field
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request,'profile.html',context)

def create_profile(request):
    if request.method=="POST":
        profile = Profile(
            user = request.user,
            profileimage=request.FILES.get('profileimage'),
            firstname=request.POST['firstname'].upper(),
            lastname=request.POST['lastname'].upper(),
            state=request.POST['state'].upper(),
            phonenumber=request.POST['phonenumber'].upper(),
        )
        profile.save()
        return redirect('home')
    return render(request,'create-profile.html')

def update_profile(request,pk):
    profile = Profile.objects.get(pk=pk)
    #context = {'profile':profile}
    if request.method == "POST":
        profile.profileimage = request.FILES.get('profileimage', profile.profileimage)
        profile.firstname = request.POST['firstname'].upper()
        profile.lastname = request.POST['lastname'].upper()
        profile.state = request.POST['state'].upper()
        profile.phonenumber = request.POST['phonenumber'].upper()
        profile.save()
        return redirect('update-profile',pk=pk)
    context = {'profile':profile}
    return render(request,'update-profile.html',context)

@login_required(login_url='loging')
def contribution(request,pk):
    month = Month.objects.get(pk=pk)
    confirmed = ConfirmPayment.objects.filter(contribution=month.contribution).first()
    
    #contributionimage = Contribution.objects.get(user=request.user)
    if request.method == "POST":
        contributionimage = request.FILES.get('contributionimage')
        months = request.POST['month'].upper()
        contribution = Contribution(user=request.user,contributionimage=contributionimage,months=months)
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
    profile = Profile.objects.all()
    return render(request,'myusers.html',{"users":users,"profile":profile})

def imagess(request):
    if request.method == "POST":
        pimage=request.FILES.get('pimage')
        bodyimage=request.FILES.get('bodyimage')
        logoimage=request.FILES.get('logoimage')
        newimage = Theimages(pimage=pimage,bodyimage=bodyimage,logoimage=logoimage)
        newimage.save()
    return render(request,'imagess.html')




    
def confirmed_users(request):
    all = ConfirmPayment.objects.all()
    themonth = Month.objects.all()
    context = {"all":all,"themonth":themonth}
    return render(request,'confirmed-users.html',context)

'''
@login_required(login_url='loging')
def notifications(request):
    all = ConfirmPayment.objects.all()
    context = {"all":all}
    return render(request,'notifications.html')
    '''

@login_required(login_url='loging')
def notifications(request):
    user = request.user
    # Filter only the contributions linked to the logged-in user
    themonth = Month.objects.all()
    all_notifications = ConfirmPayment.objects.filter(contribution__user=user).select_related('contribution')
    context = {"all": all_notifications,'themonth':themonth}
    return render(request, 'notifications.html', context)

@login_required(login_url='loging')
def order(request):
    order = OrderMade.objects.all()
    context = {'order':order}
    if request.method == "POST":
        name = request.POST['name'].upper()
        state = request.POST['state'].upper()
        address = request.POST['address'].upper()
        foodname = request.POST['foodname'].upper()
        phonenumber = request.POST['phonenumber']

        new_order = OrderMade(
            user=request.user,
            name=name,
            state=state,
            foodname=foodname,
            address=address,
            phonenumber=phonenumber
            )
        new_order.save()
        
        return redirect('order')
        
    return render(request,'order.html',context)

def all_orders(request):
    order = OrderMade.objects.all()
    context = {'order':order}
    return render(request,'all-orders.html',context)

def deleteorder(request,pk):
    order = OrderMade.objects.get(pk=pk)
    order.delete()
    return redirect('all-orders')

def about(request):
    images = AboutImages.objects.all()
    context = {'images':images}
    if request.method == "POST":
        aboutimage = request.FILES.get("aboutimage")
        new_image = AboutImages(
            aboutimage=aboutimage
        )
        new_image.save()
        return redirect('about')
    return render(request,'about.html',context)

def deleteabout(request,pk):
    order = AboutImages.objects.get(pk=pk)
    order.delete()
    return redirect('about')

def contact(request):
    all_messages = ContactMessage.objects.all()
    context = {"all_messages":all_messages}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        messag = request.POST['messag']

        new_message = ContactMessage(
            name=name,
            email=email,
            messag=messag
        )
        new_message.save()
        messages.info(request,'successfully sent')
        return redirect('contact')
    return render(request,'contact.html',context)
