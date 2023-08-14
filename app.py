from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import mysql.connector
import config
import math
import bcrypt
import re

# When you gonna start, pip install -r requirements.txt


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'aHn6Zb7MstRxC8vEoF2zG3B9wQjKl5YD'

db_conn = None
connection = None


def get_cursor():
    global db_conn
    global connection
    connection = mysql.connector.connect(user=config.dbuser,
                                         password=config.dbpass,
                                         host=config.dbhost,
                                         database=config.dbname,
                                         autocommit=True)
    db_conn = connection.cursor()
    return db_conn


first_select = get_cursor()
first_select.execute("""SELECT * FROM `city`;""")
city_list = first_select.fetchall()
first_select.execute("""SELECT * FROM `title`;""")
title_list = first_select.fetchall()
first_select.execute("""SELECT * FROM `region`;""")
region_list = first_select.fetchall()
first_select.close()


@app.route('/')
def index():
    return render_template('welcome_page.html')


# Function to display aqua aerobics class timetable
@app.route('/view_class', methods=['GET', 'POST'])
def view_class():
    sql_data = get_cursor()
    # Default dates based on today's date
    if request.method == 'GET':
        end_date = date(2023, 7, 30)
        while end_date < date.today():
            end_date += timedelta(days=7)
        start_date = end_date - timedelta(days=6)
    # Check whether the user submitted a form via POST
    else:
        # Take start_date and end_date from html, convert them into dates and carry out adding/subtracting operations
        start_date_string = request.form['start_date']
        end_date_string = request.form['end_date']
        start_time = datetime.strptime(start_date_string, "%Y-%m-%d")
        end_time = datetime.strptime(end_date_string, "%Y-%m-%d")
        start_date = start_time.date()
        end_date = end_time.date()
        # If previous week button is clicked, start_date and end_date are subtracted 7 days
        if "previous_week" in request.form:
            start_date -= timedelta(days=7)
            end_date -= timedelta(days=7)
        # If next week button is clicked, start_date and end_date are added 7 days
        elif "next_week" in request.form:
            start_date += timedelta(days=7)
            end_date += timedelta(days=7)
    # Generate a list of dates
    date_to_add = start_date
    date_list = []
    while date_to_add <= end_date:
        date_list.append(date_to_add.isoformat()[5:])
        date_to_add += timedelta(days=1)
    # Select data of every aqua aerobic class within a week
    sql = """SELECT class_id, class_name, class_date, start_time FROM class_list WHERE (is_individual=0) AND (class_date BETWEEN %s AND %s);"""
    sql_value = (start_date, end_date)
    sql_data.execute(sql, sql_value)
    sql_list = sql_data.fetchall()
    class_list = []
    # Check the weekday number of each date and append them.
    for item in sql_list:
        temp_list = list(item)  # Convert tuple into list
        weekday_number = item[2].weekday() + 1
        time = str(item[3])  # Convert time into string
        temp_list[3] = time[:-3]  # Remove seconds from the time and replace timedelta with string
        temp_list.append(weekday_number)
        class_list.append(temp_list)
    # Create time_list and row_list to display time and slots for the timetables
    time_list = ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00']
    row_list = []
    for time in time_list:
        temp_list = [time]
        for i in range(7):
            temp_list.append([])
        row_list.append(temp_list)
    # Compare class_list with time_list. Append the list with a dictionary of class_id (key) and class_name (value) if there is a class at that time.
    for item in class_list:
        for row in row_list:
            if item[3] == row[0]:
                row[item[-1]].append({item[0]: item[1]})
    sql_data.close()
    return render_template('view_class.html', class_list=class_list, date_list=date_list, row_list=row_list, start_date=start_date, end_date=end_date)


@app.route('/user_list', methods=['GET'])
def user_list():
    # if "loggedin" in session:
    if 1:
        # if session['admin'] == 1 or session['root'] == 1:
        if 1:
            sql_data = get_cursor()
            sql = """SELECT m.user_id,m.first_name,m.last_name,m.phone_number,t.title,u.username,u.email,m.state FROM member AS m
                        LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                        LEFT JOIN `title` AS t ON t.title_id=m.title_id
                        WHERE m.state = 1;"""
            sql_data.execute(sql)
            member_list = sql_data.fetchall()
            sql = """SELECT i.user_id,i.first_name,i.last_name,i.phone_number,t.title,u.username,u.email,i.state FROM instructor AS i
                        LEFT JOIN `user_account` AS u ON u.user_id=i.user_id
                        LEFT JOIN `title` AS t ON t.title_id=i.title_id
                        WHERE i.state = 1;"""
            sql_data.execute(sql)
            instructor_list = sql_data.fetchall()
            sql_data.close()
            return render_template("user_list.html", member_list=member_list, instructor_list=instructor_list)
        else:
            return url_for("/")
    else:
        return url_for("/login/")


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests   
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handle user login:
    
    1. Check if "username" and "password" POST data exist (i.e., the form has been submitted).
    2. Create variables for the username and password for easy access.
    3. Check if the username exists in the database.
    4. If the username exists, validate the hashed password against the submitted password.
    5. If passwords match, create session data for the logged-in user.
    6. Redirect the user to the appropriate dashboard based on their role.
    7. If the username or password is incorrect, inform the user.
    8. If the request is a GET request or the form hasn't been submitted, show the login form.

    """
    # Check if "username" and "password" POST requests exist (user submitted form)
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists
        cursor = get_cursor()
        cursor.execute("SELECT * FROM user_account WHERE username = %s", (username,))
        account = cursor.fetchone()
        if account is not None:
            password_hash = account[3]
            # Check if the hashed password matches the one stored in the database
            if bcrypt.checkpw(user_password.encode('utf-8'), password_hash.encode('utf-8')):
                # If the passwords match, log the user in
                session['loggedin'] = True
                session['user_id'] = account[0]
                session['username'] = account[1]
                session['is_member'] = account[4]
                session['is_instructor'] = account[5]
                session['is_admin'] = account[6]
                session['is_root'] = account[7]
                # Redirect to home page
                if session['is_root'] == 1:
                    return redirect(url_for('dashboard'))
                elif session['is_instructor'] == 1:
                    return redirect(url_for('staff_dashboard'))
                elif session['is_admin'] == 1:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('home'))
            else:
                # Add a message to prompt the use
                msg = "Incorrect password!"
        else:
            # Account doesn't exist or username incorrect
            msg = 'Incorrect username!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    """
    Handle user logout:
    
    1. Remove user-specific data from the session to log the user out.
    2. Redirect or inform the user that they have successfully logged out.
    """
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_member', None)
    session.pop('is_admin', None)
    session.pop('is_instructor', None)
    session.pop('is_root', None)

    # Add a flash message to prompt the user
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    1. Setup: Establishes the /register route for GET and POST requests.
    2. Feedback Init: Initializes an empty feedback message with msg = ''.
    3. GET Handling: On GET, retrieves titles, cities, and regions; returns the registration form.
    4. POST Handling: On POST, extracts and processes submitted form data.
    5. Validation: Checks for duplicate accounts, validates email, password, username, and birth date formats.
    6. Data Storage: If valid, hashes password, stores user data in the database, retrieves the user's ID, and saves detailed info.
    7. Feedback Setup: Sets a feedback message based on the registration outcome.
    8. Response: Renders the register.html template with the feedback message.
    
    """
    # Initial message to display to the user
    msg = ''
    today = datetime.today().date()
    # If the HTTP request is GET (i.e., the user is accessing the registration page)
    if request.method == 'POST':
        # Define the required and optional fields for registration
        required_fields = [
            'username', 'password', 'email', 'title_id', 'first_name', 'last_name',
            'phone_number', 'city_id', 'region_id', 'street_name', 'birth_date'
        ]
        optional_fields = ['detailed_information', 'health_information']

        # Ensure all necessary fields are present in the submitted form
        if not all(request.form.get(field) for field in required_fields):
            msg = "Please fill out all required fields!"
            return render_template('register.html', msg=msg)

        # Extract form values
        values = {field: request.form[field] for field in required_fields}
        for field in optional_fields:
            values[field] = request.form.get(field, None)

        # Process basic details
        username = values['username'].capitalize()
        password = values['password']
        email = values['email']
        first_name = values['first_name'].capitalize()
        last_name = values['last_name'].capitalize()

        with get_cursor() as cursor:
            # Check if provided email or username already exists in the database
            cursor.execute('SELECT email, username FROM user_account WHERE email = %s OR username = %s', (email, username,))
            existing_data = cursor.fetchone()
            # If there's a match, notify the user
            if existing_data:
                existing_email, existing_username = existing_data
                if existing_email == email:
                    msg = 'An account with this email already exists!'
                if existing_username == username:
                    msg += ' An account with this username already exists!'
            # Validation for email, password, username, name format, and birthdate
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
                msg = 'Password must contain at least 8 characters, one letter and one number!'
            elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', username):
                msg = 'Username must be at least 8 characters long and contain both characters and numbers!'
            elif not first_name.isalpha() or not last_name.isalpha():
                msg = 'First name and Last name must only contain letters!'
            elif not re.match(r'^\d{4}-\d{2}-\d{2}$', values['birth_date']):
                msg = 'Birth date must be in the format YYYY-MM-DD!'
            else:
                # Generate password hash and get current registration date
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # Insert the user's basic details into user_account
                cursor.execute("""INSERT INTO user_account (username, password, email, is_member, register_date) 
                            VALUES (%s, %s, %s, 1, %s )""", (username, hashed, email, today))
                # Get the generated user_id for the above insert
                cursor.execute('SELECT user_id from user_account WHERE username = %s', (username,))
                user_id = cursor.fetchone()[0]
                # Insert the user's detailed information into the member table
                sql = """INSERT INTO member (user_id, title_id, first_name, last_name, phone_number, 
                            city_id, region_id, street_name, birth_date, state)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)"""
                value = (user_id, values['title_id'], first_name, last_name, values['phone_number'], values['city_id'],
                         values['region_id'], values['street_name'], values['birth_date'])
                cursor.execute(sql, value)
                return redirect(url_for('login'))
        # Return the registration template with the appropriate message
    return render_template('register.html', msg=msg, titles=title_list, cities=city_list, regions=region_list, today=today)


@app.route('/instructor_change_information', methods=['GET', 'POST'])
def instructor_change_information():
    """
    The webpage used to give the instructor change his own information
    :return: instructor_change_information.html
    """

    def check_change(old, new):
        for i in range(len(new)):
            if old[i + 1] != new[i]:
                return True
        return False

    # if 'loggedIn' in session:
    if 1:
        # user_id = session["user_id"]
        user_id = 3
        sql_data = get_cursor()
        msg = ""
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            title = int(request.form.get('title'))
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            detailed_information = request.form.get('detailed_information')
            user_id = request.form.get('user_id')
            sql = """SELECT i.user_id,i.first_name,i.last_name,i.title_id,u.email,i.phone_number,i.detailed_information FROM `instructor` AS i
                        LEFT JOIN `user_account` AS u ON i.user_id=u.user_id
                        WHERE i.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            instructor_list = sql_data.fetchall()[0]
            new_data = (first_name, last_name, title, email, phone_number, detailed_information)
            if check_change(instructor_list, new_data):
                sql = """UPDATE `instructor` SET first_name=%s,last_name=%s,title_id=%s,phone_number=%s,detailed_information=%s WHERE user_id=%s;"""
                sql_value = (first_name, last_name, title, phone_number, detailed_information, user_id,)
                sql_data.execute(sql, sql_value)
                # check email
                sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
                user_account_list = sql_data.fetchall()[0]
                if email != user_account_list[1]:
                    sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                    if len(sql_data.fetchall()) > 0:
                        msg = "This email already be used."
                    else:
                        sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
            else:
                msg = "no modification"
        sql = """SELECT i.user_id,i.title_id,i.first_name,i.last_name,i.phone_number,i.detailed_information,u.email FROM `instructor` AS i
                    LEFT JOIN `user_account` AS u ON i.user_id=u.user_id
                    WHERE i.user_id=%s;"""
        sql_value = (user_id,)
        print(sql % sql_value)
        sql_data.execute(sql, sql_value)
        instructor_detail = sql_data.fetchall()[0]
        sql_data.close()
        return render_template('instructor_change_information.html', instructor_detail=instructor_detail, msg=msg, title_list=title_list)
    else:
        return redirect(url_for('login'))


@app.route('/admin_change_information', methods=['GET', 'POST'])
def admin_change_information():
    """
    The webpage used to give the admin change his own information
    :return: admin_change_information.html
    """

    def check_change(old, new):
        for i in range(len(new)):
            if old[i + 1] != new[i]:
                return True
        return False

    # if 'loggedIn' in session:
    if 1:
        # user_id = session["user_id"]
        user_id = 4
        sql_data = get_cursor()
        msg = ""
        if request.method == 'POST':
            title = int(request.form.get('title'))
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            user_id = request.form.get('user_id')
            sql = """SELECT a.user_id,a.title_id,a.first_name,a.last_name,a.phone_number,u.email FROM `admin` AS a
                        LEFT JOIN `user_account` AS u ON a.user_id=u.user_id
                        WHERE a.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            admin_list = sql_data.fetchall()[0]
            new_data = (title, first_name, last_name, phone_number, email)
            # check change
            if check_change(admin_list, new_data):
                sql = """UPDATE `admin` SET title_id=%s,first_name=%s,last_name=%s,phone_number=%s WHERE user_id=%s;"""
                value = (title, first_name, last_name, phone_number, user_id,)
                sql_data.execute(sql, value)
                # check email
                sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
                user_account_list = sql_data.fetchall()[0]
                if email != user_account_list[1]:
                    sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                    if len(sql_data.fetchall()) > 0:
                        msg = "This email already be used."
                    else:
                        sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
            else:
                msg = "No modification"
        sql = """SELECT a.user_id,a.title_id,a.first_name,a.last_name,a.phone_number,u.email FROM `admin` AS a
                    LEFT JOIN `user_account` AS u ON a.user_id=u.user_id
                    WHERE a.user_id=%s;"""
        sql_value = (user_id,)
        sql_data.execute(sql, sql_value)
        admin_list = sql_data.fetchall()[0]
        sql_data.close()
        return render_template('admin_change_information.html', admin_list=admin_list, msg=msg, title_list=title_list)


@app.route('/member_change_information', methods=['GET', 'POST'])
def member_change_information():
    """
    The webpage used to give the member change his own information
    :return: member_change_information.html
    """
    # if 'loggedIn' in session:
    if 1:
        # user_id = session["user_id"]
        user_id = 2
        sql_data = get_cursor()
        msg = ""
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            birth_date = request.form.get('birth_date')
            title = int(request.form.get('title'))
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            city = int(request.form.get('city'))
            region = int(request.form.get('region'))
            street_name = request.form.get('street_name')
            detailed_information = request.form.get('detailed_information')
            health_information = request.form.get('health_information')
            user_id = request.form.get('user_id')
            sql = """UPDATE `member` SET first_name=%s,last_name=%s,birth_date=%s,title_id=%s,phone_number=%s,city_id=%s,region_id=%s,street_name=%s,
                        detailed_information=%s, health_information=%s 
                        WHERE user_id=%s;"""
            sql_value = (first_name, last_name, birth_date, title, phone_number, city, region, street_name, detailed_information, health_information,
                         user_id,)
            sql_data.execute(sql, sql_value)
            # check email
            sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
            user_account_list = sql_data.fetchall()[0]
            if email != user_account_list[1]:
                sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                if len(sql_data.fetchall()) > 0:
                    msg = "This email already be used."
                else:
                    sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
        sql = """SELECT m.user_id,m.title_id,m.first_name,m.last_name,m.phone_number,m.detailed_information,m.city_id,
                    m.region_id,m.street_name,m.birth_date,m.health_information,u.email FROM `member` AS m
                    LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                    WHERE m.user_id=%s;"""
        sql_value = (user_id,)
        sql_data.execute(sql, sql_value)
        member_detail = sql_data.fetchall()[0]
        sql_data.close()
        return render_template('member_change_information.html', member_detail=member_detail, msg=msg, title_list=title_list, city_list=city_list,
                               region_list=region_list)
    else:
        return redirect(url_for('login'))


# Function to display details of a class
@app.route('/display_class/<class_id>')
def displayclass(class_id):
    sample_value = class_id
    sql_data = get_cursor()
    sql = """SELECT class_id, class_name, class_date, start_time, end_time, class_list.detailed_information, first_name, last_name, pool.pool_name FROM swimming_pool.class_list INNER JOIN instructor ON class_list.instructor_id=instructor.instructor_id INNER JOIN pool ON class_list.pool_id=pool.pool_id WHERE class_id=%s;"""
    sql_value = (sample_value,)
    sql_data.execute(sql, sql_value)
    detail_list = sql_data.fetchone()
    sql_data.close()
    return render_template('display_class.html', detail_list=detail_list)


if __name__ == '__main__':
    app.run(debug=True)
