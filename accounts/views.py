from django.shortcuts import redirect, render
from django.contrib import messages,auth
from contacts.models import Contact
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        email = request.POST.get('email')

        #check password
        if password == password2 and password != '':
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                # email check
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already regitered')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password,   ####
                                               first_name=first_name,last_name=last_name)        ######create_user *******
                    user.save()
                    # auth.login(request, user)
                    messages.success(request, 'Your registration was successfully')
                    return redirect('login')
        else:
            messages.error(request, 'Password Mismatch')   
            return redirect('register') 

        
        
    return render(request, 'accounts/register.html')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
    context = {'user_contacts': user_contacts}
    return render(request, 'accounts/dashboard.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)   ############ new imp
            messages.success(request, 'Login successful')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Your are now logged out')
    return redirect('index')