from django.db import connection
from django.shortcuts import redirect
from django.shortcuts import render
import random
import string


# Create your views here.
def home(request):
    return render(request, 'home.html')


def inserttrackable(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        public = request.POST.get('public')
        checkin_date = request.POST.get('checkinDate')
        tag = request.POST.get('tag')
        condition = request.POST.get('condition')
        weather = request.POST.get('weather')
        symptom = request.POST.get('symptom')
        treatment = request.POST.get('treatment')

        condition_val = request.POST.get('condition_val')
        weather_val = request.POST.get('weather_val')
        treatment_val = request.POST.get('treatment_val')
        symptom_val = request.POST.get('symptom_val')
        print(condition_val)
        with connection.cursor() as cursor:
            cursor.execute("""
                        select tag_id from Tag where name = %s
                    """, [tag])
            tag_id = cursor.fetchone()

        if tag_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Tag (name)
                            values (%s)
                        """, [tag])
                cursor.execute("SELECT LAST_INSERT_ID()")
                tag_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select condition_id from `Condition` 
                        where name = %s and value = %s
                    """, [condition, condition_val])
            condition_id = cursor.fetchone()

        if condition_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into `Condition` (name, value)
                            values (%s, %s)
                        """, [condition, condition_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                condition_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select weather_id from Weather 
                        where name = %s and value = %s
                    """, [weather, weather_val])
            weather_id = cursor.fetchone()

        if weather_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Weather (name, value)
                            values (%s, %s)
                        """, [weather, weather_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                weather_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select treatment_id from Treatment where name = %s and value = %s
                    """, [treatment, treatment_val])
            treatment_id = cursor.fetchone()

        if treatment_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Treatment (name, value)
                            values (%s, %s)
                        """, [treatment, treatment_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                treatment_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select symptom_id from Symptom where name = %s and value = %s
                    """, [symptom, symptom_val])
            symptom_id = cursor.fetchone()

        if symptom_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Symptom (name, value)
                            values (%s, %s)
                        """, [symptom, symptom_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                symptom_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Trackable (user_id, checkin_date, tag_id, condition_id, weather_id, symptom_id, treatment_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                [user_id, checkin_date, tag_id, condition_id, weather_id, symptom_id, treatment_id])
        return redirect(f'/personal/{user_id}')
    else:
        return render(request, 'inserttrackable.html')


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
            return redirect(f'/personal/{user[0]}')
    else:
        return render(request, 'login.html')


def personal(request, user_id):
    # # Get user_id from session
    # user_id = request.session.get('user_id')
    # Get user_id from session if not provided in URL
    if user_id is None:
        user_id = request.session.get('user_id')

    # Delete user data or trackable record
    if request.method == 'POST' and 'delete' in request.POST:
        trackable_id = request.POST.get('trackable_id')
        delete_action = request.POST.get('delete')

        if delete_action == 'record':
            with connection.cursor() as cursor:
                cursor.execute("""
                    delete from Trackable where trackable_id = %s
                """, [trackable_id])
        elif delete_action == 'user':
            with connection.cursor() as cursor:
                cursor.execute("delete from Trackable where user_id = %s;", [user_id])
                cursor.execute("delete from UserInfo where user_id = %s;", [user_id])
            return redirect('/login')

    with connection.cursor() as cursor:
        # Get user's info
        cursor.execute("""
            select username, email, phone, gender, age, country from UserInfo
            where user_id = %s
        """, [user_id])
        userInfo = cursor.fetchone()
        # print(userInfo[0])

        # Get user's trackable info
        cursor.execute("""
            select tra.checkin_date as checkinDate, t.name as tagname, c.name as `condition`, c.value as condition_val,
            s.name as symptom, s.value as symptom_val, tre.name as treatment, tre.value as treatment_val, 
            w.name as weather, w.value as weather_val, tra.trackable_id, user_id
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

        treatments = []
        for symptom in symptoms:
            cursor.callproc('MostEffectiveTreatment', [symptom])
            treatment_id, treatment_name, treatment_count = cursor.fetchone()
            treatments.append(treatment_name)
    # print(treatments)
    return render(request, 'personal.html', {'trackableInfo': trackableInfo,
                                             'symptoms': zip(symptoms, treatments), 'userInfo': userInfo})


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
        while True:
            # Generate random user_id until it is unique
            user_id = ''.join(random.choices(all_chars, k=8))
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM UserInfo WHERE user_id = %s", [user_id])
                row = cursor.fetchone()
                if row is None:
                    break

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

        return redirect('/login')
    else:
        return render(request, 'register.html')


def updateUser(request):
    user_id = request.session.get('user_id')
    with connection.cursor() as cursor:
        cursor.execute("""
            select * from UserInfo where user_id = %s
        """, [user_id])
        userInfo = cursor.fetchone()

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
        return render(request, 'updateUser.html', {'userInfo': userInfo})


def updateRecord(request, trackable_id):
    user_id = request.session.get('user_id')

    # Get user's trackable info
    with connection.cursor() as cursor:
        cursor.execute("""
            select w.name as weather, w.value as weather_value, s.name as symptom, s.value as symptom, 
            tre.name as treatment, tre.value as treatment_val, tra.checkin_date as checkinDate, t.name as tagname, 
            c.name as `condition`, c.value as condition_val, tra.trackable_id, user_id
            from Trackable tra
            left join `Condition` c on tra.condition_id = c.condition_id
            left join Symptom s on tra.symptom_id = s.symptom_id
            left join Treatment tre on tra.treatment_id = tre.treatment_id
            left join Tag t on tra.tag_id = t.tag_id
            left join Weather w on tra.weather_id = w.weather_id
            where user_id = %s AND trackable_id = %s
            """, [user_id, trackable_id])
        trackableInfo = cursor.fetchone()

    if request.method == 'POST':
        public = request.POST.get('public')

        checkin_date_temp = request.POST.get('checkinDate')

        tag = request.POST.get('tag')

        condition = request.POST.get('condition')
        condition_val = request.POST.get('condition_val')
        print("condition:")
        print(condition_val)
        weather = request.POST.get('weather')
        weather_val = request.POST.get('weather_val')
        
        symptom = request.POST.get('symptom')
        symptom_val = request.POST.get('symptom_val')

        treatment = request.POST.get('treatment')
        treatment_val = request.POST.get('treatment_val')

        with connection.cursor() as cursor:
            cursor.execute("""
                        select tag_id from Tag where name = %s
                    """, [tag])
            tag_id = cursor.fetchone()

        if tag_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Tag (name)
                            values (%s)
                        """, [tag])
                cursor.execute("SELECT LAST_INSERT_ID()")
                tag_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select condition_id from `Condition` 
                        where name = %s and value = %s
                    """, [condition, condition_val])
            condition_id = cursor.fetchone()

        if condition_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into `Condition` (name, value)
                            values (%s, %s)
                        """, [condition, condition_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                condition_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select weather_id from Weather 
                        where name = %s and value = %s
                    """, [weather, weather_val])
            weather_id = cursor.fetchone()

        if weather_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Weather (name, value)
                            values (%s, %s)
                        """, [weather, weather_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                weather_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select treatment_id from Treatment where name = %s and value = %s
                    """, [treatment, treatment_val])
            treatment_id = cursor.fetchone()

        if treatment_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Treatment (name, value)
                            values (%s, %s)
                        """, [treatment, treatment_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                treatment_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                        select symptom_id from Symptom where name = %s and value = %s
                    """, [symptom, symptom_val])
            symptom_id = cursor.fetchone()

        if symptom_id is None:
            with connection.cursor() as cursor:
                cursor.execute("""
                            insert into Symptom (name, value)
                            values (%s, %s)
                        """, [symptom, symptom_val])
                cursor.execute("SELECT LAST_INSERT_ID()")
                symptom_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Trackable SET checkin_date = %s, tag_id = %s, condition_id = %s, weather_id = %s, symptom_id = %s, treatment_id = %s WHERE trackable_id = %s AND user_id = %s
                           """,
                           [checkin_date_temp, tag_id, condition_id, weather_id, symptom_id, treatment_id, trackable_id,
                            user_id])
        return redirect(f'/personal/{user_id}')
    else:
        return render(request, 'updateRecord.html', {'trackableInfo': trackableInfo})


def delete_procedure(procedure_name):
    with connection.cursor() as cursor:
        cursor.execute(f"DROP PROCEDURE IF EXISTS {procedure_name};")


def square(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            select distinct name
            from Symptom
        """, [])
    symptoms = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        selected_symptom = request.POST.get('selected_symptom')
        with connection.cursor() as cursor:
            delete_procedure('GetUserInfoBySymptom')
            cursor.execute("""  
                CREATE PROCEDURE GetUserInfoBySymptom(IN symptom_name VARCHAR(255))
                BEGIN
                    SELECT u.username, u.age, u.gender, u.country, u.email, u.phone, tre.name, tre.value
                    FROM UserInfo u
                    LEFT JOIN Trackable t ON u.user_id = t.user_id
                    LEFT JOIN Treatment tre ON t.treatment_id = tre.treatment_id
                    WHERE t.symptom_id IN (
                        SELECT symptom_id
                        FROM Symptom
                        WHERE name = symptom_name
                    );
                END;
            """)
            connection.commit()
            cursor.callproc('GetUserInfoBySymptom', [selected_symptom])
            patients = cursor.fetchall()
            print(patients)

        return render(request, 'square.html', {'symptoms': symptoms, 'selected_symptom': selected_symptom, 'patients': patients})

    return render(request, 'square.html', {'symptoms': symptoms})
