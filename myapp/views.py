from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.db import connection
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
            # Save user_id to session
            request.session['user_id'] = user[0].user_id
            return redirect('/personal')

    else:
        print('get')
        return render(request, 'login.html')


def personal(request):
    # Get user_id from session
    user_id = request.session.get('user_id')
    with connection.cursor() as cursor:
        # Get user's info
        # Get user's phone and gender
        cursor.execute("""
            select email, phone, gender from UserInfo
            where user_id = %s
        """, [user_id])
        userInfo = cursor.fetchone()
        # print(userInfo[0])

        # Get user's symptoms
        cursor.execute("""
                    select distinct s.name from Symptom s
                    where symptom_id in (
                        select symptom_id from Trackable
                        where user_id = %s and symptom_id IS NOT NULL
                    )
                """, [user_id])
        symptoms = cursor.fetchall()

    return render(request, 'personal.html', {'symptoms': symptoms, 'userInfo': userInfo})
