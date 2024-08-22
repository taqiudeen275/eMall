from django.shortcuts import render,redirect,reverse
from django.contrib.auth import  authenticate,login,logout
from .forms import *

def loginView(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    next1 = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username and password is not None:
                user = authenticate(username=username,password=password)
                login(request,user)
            
                if next1:
                    return redirect(next1)
            return redirect('/products')
    context = {
        'form': form,
        
    }
    return render(request, 'login.html', context)



def signupView(request):
    form = SignupForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'POST':
        if form.is_valid():
            user =form.save(commit= False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            user = authenticate(username=user.username, password=password)
            login(request, user)
            if user.user_type == "Business":
                return redirect(reverse('business_registration'))
            return redirect('/products')
    context = {
        'form': form,
        'title': 'Register',
    }
    return render(request, 'register.html', context)


def logoutView(request):
    logout(request)
    return redirect('/')

# @login_required
# def profile(request):
#     form = ProfileForm(request.POST or None,request.FILES or None, instance=request.user)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#     context = {
#         'form': form,
#         'title': 'Profile',
#     }
#     user = request.user
#     if user.user_type == 'staff':
#         staff = get_object_or_404(Staff, user=request.user)
#         if not staff.verified :
#             return redirect('staffUser:register')
#         staff_form = StaffForm(request.POST or None, instance=staff)
#         context.update({'staff_form':staff_form,  'staff':staff})

#     if user.user_type == 'student':
#         studentUser = get_object_or_404(StudentUser, user=request.user)
#         if not studentUser.verified:
#             return redirect('studentUser:register')
#         student = get_object_or_404(Student, user=request.user)
#         student_form = StudentForm(request.POST or None, request.FILES or None, instance=student)
#         context.update({'student_form':student_form,  'student':student})

#     if user.user_type == 'parent':
#         parentUser = get_object_or_404(Parent, user=request.user)
#         if not parentUser.verified:
#             messages.error(request, 'verify your account')
#             return redirect('parentUser:register')
#         context.update({'parent':parentUser})
    
#     return render(request, 'account/profile.html', context)
