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

    # Delete user data or trackable record
    if request.method == 'POST' and 'delete' in request.POST:
        trackable_id = request.POST.get('trackable_id')
        delete_action = request.POST.get('delete')

        # print(trackable_id)

        if delete_action == 'record':
            with connection.cursor() as cursor:
                cursor.execute("""
                    delete from Trackable where trackable_id = %s
                """, [trackable_id])
        elif delete_action == 'user':
            with connection.cursor() as cursor:
                cursor.execute("""
                    delete from UserInfo where user_id = %s
                """, [user_id])
            return redirect('/login')

    # if request.method == 'POST' and 'update' in request.POST:
    #     trackable_id = request.POST.get('trackable_id')
    #
    #     public = request.POST.get('public')
    #     checkin_date = request.POST.get('checkin_date')
    #     tag = request.POST.get('tag')
    #     condition = request.POST.get('Condition')
    #     weather = request.POST.get('weather')
    #     treatment = request.POST.get('treatment')
    #     symptom = request.POST.get('symptom')
    #
    #     with connection.cursor() as cursor:
    #         cursor.execute("""
    #                     UPDATE Trackable
    #                     SET public = %s, checkin_date = %s, tag = %s, condition = %s, weather = %s, treatment = %s, symptom = %s
    #                     WHERE trackable_id = %s
    #                 """, [public, checkin_date, tag, condition, weather, treatment, symptom, trackable_id])

    with connection.cursor() as cursor:
        # Get user's info
        cursor.execute("""
            select email, phone, gender from UserInfo
            where user_id = %s
        """, [user_id])
        userInfo = cursor.fetchone()
        # print(userInfo[0])

        # Get user's trackable info
        cursor.execute("""
            select tra.checkin_date as checkinDate, t.name as tagname, c.name as `condition`,
             w.name as weather, s.name as symptom, tre.name as treatment, tra.trackable_id, user_id
            from Trackable tra
            left join `Condition` c on tra.condition_id = c.condition_id
            left join Symptom s on tra.symptom_id = s.symptom_id
            left join Treatment tre on tra.treatment_id = tre.treatment_id
            left join Tag t on tra.tag_id = t.tag_id
            left join Weather w on tra.weather_id = w.weather_id
            where user_id = %s
        """, [user_id])
        trackableInfo = cursor.fetchall()

        # Get user's symptoms
        cursor.execute("""
                    select distinct s.name from Symptom s
                    where symptom_id in (
                        select symptom_id from Trackable
                        where user_id = %s and symptom_id IS NOT NULL
                    )
                """, [user_id])
        symptoms = cursor.fetchall()

    return render(request, 'personal.html', {'trackableInfo': trackableInfo,
                                             'symptoms': symptoms, 'userInfo': userInfo})


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


def updateUser(request):
    user_id = request.session.get('user_id')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        age = request.POST.get('age')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE UserInfo
                SET username = %s, email = %s, phone = %s, password = %s, gender = %s, country = %s, age = %s
                WHERE user_id = %s
            """, [username, email, phone, password, gender, country, age, user_id])

        return redirect('/login')

    else:
        return render(request, 'updateUser.html')


def updateRecord(request, trackable_id):
    if request.method == 'POST':
        public = request.POST.get('public')
        checkin_date = request.POST.get('checkin_date')
        tag = request.POST.get('tag')

        condition_name = request.POST.get('condition_name')
        condition_val = request.POST.get('condition_val')

        weather_name = request.POST.get('weather_name')
        weather_val = request.POST.get('weather_val')

        treatment_name = request.POST.get('treatment_name')
        treatment_val = request.POST.get('treatment_val')
        treatment_unit = request.POST.get('treatment_unit')

        symptom_name = request.POST.get('symptom_name')
        symptom_val = request.POST.get('symptom_val')

        tag_id, condition_id, weather_id, treatment_id, symptom_id = "", "", "", "", ""

        with connection.cursor() as cursor:
            cursor.execute("""
                select tag_id from Tag where name = %s
            """, [tag])
            tag_id = cursor.fetchone()

        if tag_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                    insert into Tag where name = %s
                """, [tag])
                cursor.execute("SELECT LAST_INSERT_ID()")
                tag_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                select condition_id from Condition where name = %s and value = %s
            """, [condition_name, condition_val])
            condition_id = cursor.fetchone()

        if condition_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                    insert into Condition where name = %s and value = %s
                """, [condition_name, condition_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                condition_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                select weather_id from Weather where name = %s and value = %s
            """, [weather_name, weather_val])
            weather_id = cursor.fetchone()

        if weather_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                    insert into Weather where name = %s and value = %s
                """, [weather_name, weather_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                weather_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                select treatment_id from Treatment where name = %s and value = %s and unit = %s
            """, [treatment_name, treatment_val, treatment_unit])
            treatment_id = cursor.fetchone()

        if treatment_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                    insert into Treatment where name = %s and value = %s and unit = %s
                """, [treatment_name, treatment_val, treatment_unit])
                cursor.execute("SELECT LAST_INSERT_ID()")
                treatment_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                select symptom_id from Symptom where name = %s and value = %s
            """, [symptom_name, symptom_val])
            symptom_id = cursor.fetchone()

        if symptom_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                    insert into Symptom where name = %s and value = %s
                """, [symptom_name, symptom_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                symptom_id = cursor.fetchone()[0]

        # Update
        with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Trackable
                    SET public = %s, checkin_date = %s, tag_id = %s, condition_id = %s, weather_id = %s, treatment_id = %s, symptom_id = %s
                    WHERE trackable_id = %s
                """, [public, checkin_date, tag_id, condition_id, weather_id, treatment_id, symptom_id, trackable_id])

        return redirect('/personal')
    else:
        return render(request, 'updateRecord.html')
