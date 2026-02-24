from django.shortcuts import render, redirect
from django.contrib.auth import login , logout, authenticate


def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            error_message = 'Введён неверный логин или пароль'
    return render(request, 'login.html' , {'error_message' : error_message})

def logout_view(request):
    logout(request)
    return redirect('login')