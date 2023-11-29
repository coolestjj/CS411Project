from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from myapp.models import Userinfo


# Create your views here.
def home(request):
    return render(request, 'home.html')


def login_(request):
    if request.method == 'POST':
        print('post')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print('email:', email)
        print('password:', password)
        user = Userinfo.objects.raw('select * from UserInfo where email = %s and password = %s', [email, password])

        if len(list(user)) == 0:
            print('user not found')
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        else:
            print('user found')
            return render(request, 'personal.html', {'userInfo': user[0]})

    else:
        print('get')
        return render(request, 'login.html')


def personal(request):
    return render(request, 'personal.html')
