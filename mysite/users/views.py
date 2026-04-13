from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required   
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.
def auth(requests):
    form=NewUserForm()
    if requests.method=='POST':
        form=NewUserForm(requests.POST)
        if form.is_valid():
            user = form.save()
            print("USER CREATED:", user)
        else:
            print(form.errors)

        return redirect('users:login')    

    context={
        'form':form
    }
    return render(requests,'users/auth.html',context)
@login_required
def profile(request):
    return render(request,'users/profile.html')

def seller_profile(request,id):
    seller_profile=User.objects.get(id=id)
    context={
        "seller_profile":seller_profile  
    }   
    return render(request,'users/seller_profile.html',context)    
@login_required    
def CreateProfile(request,user_id):
    if request.method=='POST':
        user=User.objects.get(id=user_id)
        if not user.profile :
            profile=Profile(user=user)
        if request.FILES.get('profile'):
            user.profile.image=request.FILES['profile']
        user.profile.contact_number=request.POST.get('contact')
        user.profile.save()
        return redirect('users:profile')
        # image=request.FILES['profile']
        # contact=request.POST.get('contact')
        # profile=Profile(user=request.user,image=image,contact_number=contact)
        # profile.save()
        # return redirect('users:profile')
    return render(request,'users/createprofile.html')
    