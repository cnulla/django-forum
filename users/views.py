from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if request.POST['username'] != '' or request.POST['password1'] != '' or request.POST['password2'] != '':
            if form.is_valid():
                new_user = form.save()
                authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
                login(request, authenticated_user)
            return HttpResponseRedirect(reverse('forum:index'))
        else:
            messages.error(request, 'You left one or more field(s) blank')
            
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))        
    else:
        return HttpResponseRedirect(reverse('forum:index'))


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'users/logout.html')
    else:
        return HttpResponseRedirect(reverse('forum:index'))
