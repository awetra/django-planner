from django.shortcuts import render, redirect
from django.contrib import auth


def log_in(request):

    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(
            username=username,
            password=password
        )
        
        if user:
            auth.login(request, user)
            return redirect('tasks_list')

        context['auth_errors'] = True

    return render(request, 'login.html', context)


def log_out(request):
    auth.logout(request)
    return redirect('login')