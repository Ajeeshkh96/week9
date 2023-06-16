from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.decorators import login_required
from .models import UserDetails
from django.core.cache import cache
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q


def home(request):
    return render(request, 'index.html')

################## user ############################################################

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        age = request.POST.get('age')
        addr = request.POST.get('addr')
        mob_no = request.POST.get('mob_no')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            error_message = 'Password Miss match'
            return render(request, 'signup.html', {'error_message': error_message})

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists. Please choose a different username.'
            return render(request, 'signup.html', {'error_message': error_message})

        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()

        ud = UserDetails(user=user, age=age, addr=addr, mob_no=mob_no)
        ud.save()
        
        messages.success(request, "your account has been created successfully")
        return redirect("signin")

    return render(request, 'signup.html')



@cache_control(must_revalidate=True, no_transform=True, no_cache=True, no_store=True)
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        # print('us,pas=',username,password)
        
        if username and password:
            try:
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_staff:
                        request.session['user_id'] = user.id
                        login(request, user)
                        return redirect('admin_home')  
                    else:
                        request.session['user_id'] = user.id
                        login(request, user)
                        return redirect('user_home')
                else:
                    messages.error(request, "Incorrect username or password")
                    return redirect('signin')
            except:
                pass

    return render(request, 'signin.html')


@login_required(login_url='/login')
def signout(request):
    logout(request)
    request.session.flush()
    messages.info(request, "Logout Successful")
    return redirect(reverse('signin'))


@login_required(login_url='/login')
def user_home(request):
    return render(request, 'user_home.html')


@login_required(login_url='/login')
def admin_home(request):
    return render(request, 'admin_home.html')



@login_required(login_url='/login')
def user_profile_view(request):
    user_id =  request.session['user_id']
    ud = User.objects.get(id=user_id)
    ud1 = UserDetails.objects.get(user=ud.id)
    return render(request, 'user_profile_view.html', {'ud': ud, 'ud1': ud1})



@login_required(login_url='/login')
def admin_user_details_view(request):
    ud = User.objects.exclude(is_staff=True)
    ud1 = UserDetails.objects.all()
    return render(request, 'admin_user_details_view.html', {'ud': ud, 'ud1': ud1})


@login_required(login_url='/login')
def admin_user_details_edit(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        age = request.POST['age']
        addr = request.POST['addr']
        mob_no = request.POST['mob_no']
        email = request.POST['email']
        id = request.POST['id']

        ud = User.objects.get(id=id)
        ud.username=username
        ud.first_name=fname
        ud.last_name=lname
        ud.email=email
        ud.save()

        ud1 = UserDetails.objects.get(user=id)
        ud1.age = age
        ud1.addr = addr
        ud1.mob_no = mob_no
        ud1.save()

        return render(request, 'admin_user_details_edit.html',{'msg': 'Record Updated'})
    else:
        id = request.GET['id']
        ud = User.objects.get(id=id)
        ud1 = UserDetails.objects.get(user=ud.id)
        return render(request, 'admin_user_details_edit.html', {'ud': ud, 'ud1': ud1, 'id': id})


@login_required(login_url='/login')
def admin_user_details_delete(request):
    id = request.GET['id']
    ud=User.objects.get(id=id)
    ud.delete()
    ud=User.objects.exclude(is_staff=True)
    ud1=UserDetails.objects.all()
    return render(request, 'admin_user_details_view.html', {'ud': ud, 'ud1': ud1, 'msg': 'Record deleted'})


@login_required(login_url='/login')
def admin_user_search(request):
    query = request.GET['query']
    # ud = User.objects.filter(first_name__contains=query, is_staff=False)
    ud = User.objects.filter(Q(first_name__contains=query)|Q(last_name__contains=query),Q(is_staff=False))
    ud1 = UserDetails.objects.all()
    return render(request, 'admin_user_details_view.html',{'ud': ud, 'ud1': ud1})


@login_required(login_url='/login')
def admin_user_details_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        age = request.POST.get('age')
        addr = request.POST.get('addr')
        mob_no = request.POST.get('mob_no')
        email = request.POST.get('email')
        pass1 = '1234'

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists. Please choose a different username.'
            return render(request, 'admin_user_details_add.html', {'error_message': error_message})

        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()

        ud = UserDetails(user=user, age=age, addr=addr, mob_no=mob_no)
        ud.save()
        
        messages.success(request, "your account has been created successfully")
        return redirect("/admin_user_details_add")

    return render(request, 'admin_user_details_add.html')
