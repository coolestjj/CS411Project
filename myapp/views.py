from django.db import connection
from django.shortcuts import redirect
from django.shortcuts import render
import random
import string

# Create your views here.
def home(request):
    return render(request, 'home.html')


def login_(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("""
                select * from UserInfo where email = %s and password = %s
            """, [email, password])
            user = cursor.fetchone()

        if user is None:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        else:
            request.session['user_id'] = user[0]  # user_id is the first column
            return redirect('/personal')
    else:
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


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        age = request.POST.get('age')

        # Generate random user_id of 8 characters
        all_chars = string.ascii_letters + string.digits
        user_id = ''.join(random.choices(all_chars, k=8))

        # Check if email already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM UserInfo WHERE email = %s", [email])
            row = cursor.fetchone()
            if row is not None:
                return render(request, 'register.html', {'error': 'Email already exists!'})

        # insert into UserInfo
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO UserInfo (user_id, username, email, phone, password, gender, country, age, role_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 2)",
                [user_id, username, email, phone, password, gender, country, age])

        return render(request, 'register.html', {'success': 'Register successfully!'})
    else:
        return render(request, 'register.html')
